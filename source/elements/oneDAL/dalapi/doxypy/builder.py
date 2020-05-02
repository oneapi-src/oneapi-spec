import os
import re
import sys

from typing import (
    Any,
    Dict,
    List,
    Text,
    Union,
)

from . import model
from . import utils
from .parser.compound import compounddefType as _CompoundDefType

def build(BuilderType, *args, **kwargs):
    return BuilderType(*args, **kwargs).build()

class _BuilderMixins(object):
    def __init__(self, src):
        assert src
        self.src = src

    def textify(self, text_like) -> Text:
        return self._read_inner_text(text_like).strip()

    def split_compound_name(self, compoundname):
        return utils.split_compound_name(compoundname)

    def find_parent(self, matcher):
        current = self.src
        while current:
            current = current.parent_object_
            if matcher(current):
                return current

    def build_doc(self):
        brief = self.src.briefdescription
        detailed = self.src.detaileddescription
        description = detailed if len(detailed.para) > 0 else brief
        return build(DocBuilder, description)

    def build_template(self):
        template_params = self._build_template_parameters()
        template_decl = self._build_template_declaration(template_params)
        return template_decl, template_params

    def build_location(self):
        if self.src.location:
            return build(LocationBuilder, self.src.location)

    @utils.return_list
    def _build_template_parameters(self):
        if self.src.templateparamlist:
            for param in self.src.templateparamlist.param:
                yield build(ParameterBuilder, param, is_template=True)

    def _build_template_declaration(self, template_parameters):
        template_entries = []
        for param in template_parameters:
            template_entry = f'{param.type} {param.name}'
            if param.default:
                template_entry += f' = {param.default}'
            template_entries.append(template_entry)
        return (f'template <{", ".join(template_entries)}>'
                if template_entries else None)

    def _read_inner_text(self, text_like) -> Text:
        text = ''
        if isinstance(text_like, str):
            text = text_like
        elif hasattr(text_like, 'content_'):
            for content in text_like.content_:
                text += self._read_inner_text(content.value)
        elif hasattr(text_like, 'valueOf_'):
            text = text_like.valueOf_
        return text


class DescriptionBuilder(_BuilderMixins):
    def build(self):
        return model.Description(
            runs = self._build_runs(),
        )

    @utils.return_list
    def _build_runs(self):
        content_ = (content for para in self.src.para
                            for content in para.content_)
        for content in content_:
            if content.name == 'computeroutput':
                code = self.textify(content.value)
                yield model.Run(code, 'code')
            if content.name == 'formula':
                code = self.textify(content.value)
                yield model.Run(code, 'math')
            elif not content.name:
                if content.value.strip():
                    yield from self._split_math(content.value)

    def _split_math(self, text):
        for i, chunk in enumerate(text.split('$')):
            if i % 2 and chunk:
                yield model.Run(chunk, 'math')
            elif chunk:
                yield model.Run(chunk, 'text')


class LocationBuilder(_BuilderMixins):
    def build(self):
        return model.Location(
            file = self.src.file,
            line = int(self.src.line) if self.src.line else None,
            bodyfile = self.src.bodyfile if self.src.bodyfile else None,
            bodystart = int(self.src.bodystart) if self.src.bodystart else None,
            bodyend = int(self.src.bodyend) if self.src.bodyend else None,
        )


class DocBuilder(_BuilderMixins):
    def build(self):
        return model.Doc(
            description = build(DescriptionBuilder, self.src),
            invariants = self._build_simplesect('invariant'),
            preconditions = self._build_simplesect('pre'),
            postconditions = self._build_simplesect('post'),
            remarks = self._build_simplesect('remark'),
        )

    @utils.return_list
    def _build_simplesect(self, kind: str):
        for para in self._filter_simplesect_para(kind):
            yield self.textify(para)

    def _filter_simplesect_para(self, kind: str):
        return (para_inner
            for para in self.src.para
            for simplesect in para.simplesect
                if simplesect.kind == kind
            for para_inner in simplesect.para
        )


class ParameterBuilder(_BuilderMixins):
    def __init__(self, src, is_template=False):
        super().__init__(src)
        self.is_template = is_template

    def build(self):
        name = self.textify(self.src.declname)
        type_ = self.textify(self.src.type_)
        default = self.textify(self.src.defval)
        # Sometimes, Doxygen fuses the type with the name
        # of template parameter and stores it in the `type` field.
        if not name and self.is_template:
            try:
                type_, name = type_.rsplit(' ', 1)
            except ValueError:
                pass
        return model.Parameter(
            name = name if name else None,
            type = type_ if type_ else None,
            default = default if default else None,
            description = self._build_description(name),
        )

    def _build_description(self, param_name):
        try:
            doc = self._find_parent_doc()
            param_desc = self._find_param_description(doc, param_name)
            return build(DescriptionBuilder, param_desc)
        except (AttributeError, IndexError):
            pass

    def _find_param_description(self, doc, param_name):
        param_kind = 'templateparam' if self.is_template else 'param'
        param_list = self._find_parameter_list(doc, param_kind)
        for parameteritem in param_list.parameteritem:
            parametername = parameteritem.parameternamelist[0].parametername[0]
            if self.textify(parametername) == param_name:
                return parameteritem.parameterdescription

    def _find_parent_doc(self):
        def has_detailed_description(node):
            return hasattr(node, 'detaileddescription')
        parent = self.find_parent(has_detailed_description)
        return parent.detaileddescription

    def _find_parameter_list(self, doc, kind):
        parameterlist_ = (parameterlist
            for para in doc.para
            for parameterlist in para.parameterlist
        )
        for parameterlist in parameterlist_:
            if parameterlist.kind == kind:
                return parameterlist


class FunctionBuilder(_BuilderMixins):
    def build(self):
        name = self.textify(self.src.name)
        argstring = self.textify(self.src.argsstring)
        return_type = self.textify(self.src.type_)
        template_decl, template_params = self.build_template()
        decl = self._build_declaration(template_decl, return_type,
                                       name, argstring)
        parent_fqn, fqn = self._build_fqn(name)
        return model.Function(
            doc = self.build_doc(),
            name = name,
            location = self.build_location(),
            argstring = argstring,
            parameters = self._build_params(),
            declaration = decl,
            return_type = return_type,
            template_parameters = template_params,
            template_declaration = template_decl,
            fully_qualified_name = fqn,
            parent_fully_qualified_name = parent_fqn,
        )

    @utils.return_list
    def _build_params(self):
        for param in self.src.param:
            yield build(ParameterBuilder, param)

    def _build_declaration(self, template_decl, return_type, name, argstring):
        decl = ''
        if template_decl:
            decl += template_decl + ' '
        if return_type:
            decl += return_type + ' '
        decl += name + argstring
        return decl

    def _build_fqn(self, name):
        compound = self._find_parent_compound()
        parent_fqn = self.textify(compound.compoundname)
        fqn = f'{parent_fqn}::{name}' if parent_fqn else name
        return parent_fqn, fqn

    def _find_parent_compound(self):
        def compound_matcher(node):
            return isinstance(node, _CompoundDefType)
        return self.find_parent(compound_matcher)


class ClassBuilder(_BuilderMixins):
    def build(self):
        fqn = self.textify(self.src.compoundname)
        namespace, name = self.split_compound_name(fqn)
        template_decl, template_params = self.build_template()
        decl = self._build_declaration(template_decl, name)
        return model.Class(
            doc = self.build_doc(),
            name = name,
            kind = self.textify(self.src.kind),
            location = self.build_location(),
            functions = self._build_methods(),
            declaration = decl,
            template_parameters = template_params,
            template_declaration = template_decl,
            fully_qualified_name = fqn,
            parent_fully_qualified_name = namespace,
        )

    @utils.return_list
    def _build_methods(self):
        public_func_memberdef = (memberdef
            for sectiondef in self.src.sectiondef
                if sectiondef.kind == 'public-func'
            for memberdef in sectiondef.memberdef
                if memberdef.kind == 'function'
        )
        for memberdef in public_func_memberdef:
            yield build(FunctionBuilder, memberdef)

    def _build_declaration(self, template_decl, name):
        decl = ''
        if template_decl:
            decl += template_decl + ' '
        decl += f'class {name}'
        return decl

    def _public_func_memberdef(self):
        return (
        )


class NamespaceBuilder(_BuilderMixins):
    def build(self):
        fqn = self.textify(self.src.compoundname)
        parent_name, name = self.split_compound_name(fqn)
        return model.Namespace(
            doc = self.build_doc(),
            name = name,
            location = self.build_location(),
            functions = self._build_functions(),
            fully_qualified_name = fqn,
            parent_fully_qualified_name = parent_name,
        )

    @utils.return_list
    def _build_functions(self):
        func_memberdef = (memberdef
            for sectiondef in self.src.sectiondef
                if sectiondef.kind == 'func'
            for memberdef in sectiondef.memberdef
                if memberdef.kind == 'function'
        )
        for memberdef in func_memberdef:
            yield build(FunctionBuilder, memberdef)


class ModelBuilder(_BuilderMixins):
    builder_map = {
        'class': ClassBuilder,
        'struct': ClassBuilder,
        'func': FunctionBuilder,
        'namespace': NamespaceBuilder,
    }

    def build(self):
        allowed_kinds = ModelBuilder.builder_map.keys()
        if self.src.kind not in allowed_kinds:
            raise ValueError(f'Unexpected kind of Doxygen\'s compounddef "{self.src.kind}" ',
                             f'only {", ".join(sorted(allowed_kinds))} are supported')
        BuilderType = ModelBuilder.builder_map[self.src.kind]
        return build(BuilderType, self.src)