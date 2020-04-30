from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.statemachine import ViewList
from .generator import RstBuilder

def directive(cls):
    class DirectiveFactory(cls):
        def __init__(self, ctx):
            self._ctx = ctx
        def __call__(self, *args, **kwargs):
            return cls(self._ctx, *args, **kwargs)
    return DirectiveFactory

class BaseDirective(Directive):
    def __init__(self, ctx, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ctx = ctx

class MacroDirective(BaseDirective):
    def init(self): ...
    def rst(self, x: RstBuilder): ...

    def run(self):
        self.init()
        content = ViewList()
        self._get_rst(content)
        node = nodes.section()
        node.document = self.state.document
        self.state.nested_parse(content, 0, node)
        return node.children

    def _get_rst(self, placeholder):
        x = RstBuilder(placeholder, self.ctx.current_docname, self.lineno)
        self.rst(x)


class DoxyDirective(MacroDirective):
    def init(self):
        self.ctx.watcher.link_docname(self.ctx.current_docname)

    def format_description(self, desc_def):
        rst = ''
        for run in desc_def.runs:
            if run.kind == 'text':
                rst += run.content
            elif run.kind == 'math':
                rst += f':math:`{run.content}`'
            elif run.kind == 'code':
                rst += f':cpp:expr:`{run.content}`'
        return rst.strip()

    def add_description(self, description, x: RstBuilder, level=0):
        desc_str = self.format_description(description)
        if desc_str:
            x.add_doc(desc_str, level=level)

    def add_function_base(self, func, x: RstBuilder, is_free=True, level=0):
        namespace = func.parent_fully_qualified_name if is_free else None
        x.add_function(func.declaration, namespace, level=level)
        if func.doc and func.doc.description:
            self.add_description(func.doc.description, x, level=level + 1)
        self.add_params('tparam', func.template_parameters, x, level=level + 1)
        self.add_params('param', func.parameters, x, level=level + 1)
        x.add_blank_like()

    def add_params(self, tag, params, x: RstBuilder, level=0):
        for param in params:
            if param.description:
                desc_str = self.format_description(param.description)
                x.add_param(tag, param.name, desc_str, level=level)

    def add_listing(self, model_object, x: RstBuilder):
        listing = self.ctx.listing.read(model_object)
        x.add_code_block(listing)


@directive
class ClassDirective(DoxyDirective):
    required_arguments = 1
    optional_arguments = 0
    has_content = False

    def rst(self, x: RstBuilder):
        class_ = self.ctx.index.find(self.arguments[0])
        self.add_listing(class_, x)
        sphinx_class_decl = (f'{class_.template_declaration} {class_.name}'
                             if class_.template_declaration else class_.name)
        x.add_class(sphinx_class_decl, class_.parent_fully_qualified_name)
        self.add_params('tparam', class_.template_parameters, x, level=1)
        x.add_blank_like()
        self.add_constructors(class_, x)
        self.add_methods(class_, x)
        self.add_properties(class_, x)

    def add_constructors(self, class_, x: RstBuilder):
        ctors = [func for func in class_.functions
                 if not func.return_type.strip()]
        if ctors:
            x.add('**Constructors**', level=1)
            x.add_blank_like()
        for ctor in ctors:
            self.add_function_base(ctor, x, level=1)

    def add_methods(self, class_, x: RstBuilder):
        methods = [func for func in class_.functions
                   if func.return_type.strip()]
        if methods:
            x.add('**Public Methods**', level=1)
            x.add_blank_like()
        for method in methods:
            self.add_function_base(method, x, level=1)

    def add_properties(self, class_def, x: RstBuilder):
        if class_def.properties:
            x.add('**Properties**', level=1)
            x.add_blank_like()
        for property_def in class_def.properties:
            self.add_property(property_def, x)

    def add_property(self, property_def, x: RstBuilder):
        x.add_member(property_def.declaration, level=1)
        if property_def.doc and property_def.doc.description:
            desc = self.format_description(property_def.doc.description)
            x.add_doc(desc, level=2)
        if property_def.getter or property_def.setter:
            x('Getter & Setter', level=2)
            if property_def.getter:
                x(f'| ``{property_def.getter.declaration}``', level=3)
            if property_def.setter:
                x(f'| ``{property_def.setter.declaration}``', level=3)
            x()
        if property_def.doc:
            invariants = property_def.doc.invariants
            if invariants and len(invariants) > 0:
                x('Invariants', level=2)
                for invariant in invariants:
                    x(f'| :cpp:expr:`{invariant}`', level=3)
                x()


@directive
class FunctionDirective(DoxyDirective):
    required_arguments = 1
    optional_arguments = 0
    has_content = False

    def rst(self, x: RstBuilder):
        func = self.ctx.index.find(self.arguments[0])
        # TODO: Add option to include listing
        # self.add_listing(func, x)
        self.add_function_base(func, x, is_free=True)


@directive
class ListingDirective(DoxyDirective):
    required_arguments = 1
    optional_arguments = 0
    has_content = False

    def rst(self, x: RstBuilder):
        model_object = self.ctx.index.find(self.arguments[0])
        listing = self.ctx.listing.read(model_object)
        x.add_code_block(listing)
