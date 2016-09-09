<!- This is a customized mako template for use by pdoc to render sample docs -->
<%

  import re
  import sys
  import markdown
  import pdoc

  # From language reference, but adds '.' to allow fully qualified names.
  pyident = re.compile('^[a-zA-Z_][a-zA-Z0-9_.]+$')
  indent = re.compile('^\s*')

  # Whether we're showing the module list or a single module.
  module_list = 'modules' in context.keys()

  def eprint(s):
      print >> sys.stderr, s

  def decode(s):
      if sys.version_info[0] < 3 and isinstance(s, str):
          return s.decode('utf-8', 'ignore')
      return s

  def ident(s):
      return '<span class="ident">%s</span>' % s

  def sourceid(dobj):
      return 'source-%s' % dobj.refname

  def clean_source_lines(lines):
      """
      Cleans the source code so that pygments can render it well.

      Returns one string with all of the source code.
      """
      base_indent = len(indent.match(lines[0]).group(0))
      lines = [line[base_indent:] for line in lines]
      return '<pre class="line-numbers"><code class="fbcode language-python">%s</code></pre>' % (''.join(lines))

  def linkify(match):
      matched = match.group(0)
      ident = matched[1:-1]
      name, url = lookup(ident)
      if name is None:
          return matched
      return '[`%s`](%s)' % (name, url)

  def mark(s, linky=True):
      if linky:
        s, _ = re.subn('\b\n\b', ' ', s)
        if not module_list:
            s, _ = re.subn('`[^`]+`', linkify, s)

      extensions = []
      s = markdown.markdown(s.strip(), extensions=extensions)
      return s

  def glimpse(s, length=100):
      if len(s) < length:
          return s
      return s[0:length] + '...'

  def module_url(m):
      """
      Returns a URL for `m`, which must be an instance of `Module`.
      Also, `m` must be a submodule of the module being documented.

      Namely, '.' import separators are replaced with '/' URL
      separators. Also, packages are translated as directories
      containing `index.html` corresponding to the `__init__` module,
      while modules are translated as regular HTML files with an
      `.m.html` suffix. (Given default values of
      `pdoc.html_module_suffix` and `pdoc.html_package_name`.)
      """
      if module.name == m.name:
          return ''

      if len(link_prefix) > 0:
          base = m.name
      else:
          base = m.name[len(module.name)+1:]
      url = base.replace('.', '/')
      if m.is_package():
          url += '/%s' % pdoc.html_package_name
      else:
          url += pdoc.html_module_suffix
      return link_prefix + url

  def external_url(refname):
      """
      Attempts to guess an absolute URL for the external identifier
      given.

      Note that this just returns the refname with an ".ext" suffix.
      It will be up to whatever is interpreting the URLs to map it
      to an appropriate documentation page.
      """
      return '/%s.ext' % refname

  def is_external_linkable(name):
      return external_links and pyident.match(name) and '.' in name

  def lookup(refname):
      """
      Given a fully qualified identifier name, return its refname
      with respect to the current module and a value for a `href`
      attribute. If `refname` is not in the public interface of
      this module or its submodules, then `None` is returned for
      both return values. (Unless this module has enabled external
      linking.)

      In particular, this takes into account sub-modules and external
      identifiers. If `refname` is in the public API of the current
      module, then a local anchor link is given. If `refname` is in the
      public API of a sub-module, then a link to a different page with
      the appropriate anchor is given. Otherwise, `refname` is
      considered external and no link is used.
      """
      d = module.find_ident(refname)
      if isinstance(d, pdoc.External):
          if is_external_linkable(refname):
              return d.refname, external_url(d.refname)
          else:
              return None, None
      if isinstance(d, pdoc.Module):
          return d.refname, module_url(d)
      if module.is_public(d.refname):
          return d.name, '#%s' % d.refname
      return d.refname, '%s#%s' % (module_url(d.module), d.refname)

  def link(refname):
      """
      A convenience wrapper around `href` to produce the full
      `a` tag if `refname` is found. Otherwise, plain text of
      `refname` is returned.
      """
      name, url = lookup(refname)
      if name is None:
          return refname
      return '<a href="%s">%s</a>' % (url, name)
%>
<%def name="show_source(d)">
  % if not (isinstance(d, pdoc.Module) or isinstance(d, pdoc.Class)) and show_source_code and d.source is not None and len(d.source) > 0:
    <p class="source_link"><a href="javascript:void(0);" onclick="toggle('${sourceid(d)}', this);">Hide source.</a></p>
    <div id="${sourceid(d)}" class="source" style="display: block;">
      ${decode(clean_source_lines(d.source))}
    </div>
    <hr>
  % endif
</%def>

<%def name="show_desc(d, limit=None)">
  <%
    inherits = (hasattr(d, 'inherits')
                   and (len(d.docstring) == 0
                        or d.docstring == d.inherits.docstring))
    docstring = (d.inherits.docstring if inherits else d.docstring).strip()
    if limit is not None:
        docstring = glimpse(docstring, limit)
  %>
  % if len(docstring) > 0:
    % if inherits:
      <div class="desc inherited">${docstring | mark}</div>
    % else:
      <div class="desc">${docstring | mark}</div>
    % endif
  % endif
  % if not isinstance(d, pdoc.Module):
    <div class="source_cont">${show_source(d)}</div>
  % endif
</%def>

<%def name="show_inheritance(d)">
  % if hasattr(d, 'inherits'):
      <p class="inheritance">
         <strong>Inheritance:</strong>
         % if hasattr(d.inherits, 'cls'):
           <code>${link(d.inherits.cls.refname)}</code>.<code>${link(d.inherits.refname)}</code>
         % else:
           <code>${link(d.inherits.refname)}</code>
         % endif
      </p>
  % endif
</%def>

<%def name="show_module_list(modules)">
<h1>My Module</h1>

% if len(modules) == 0:
    <p>No modules found.</p>
% else:
    <table id="module-list">
    % for name, desc in modules:
        <tr>
          <td><a href="${link_prefix}${name}">${name}</a></td>
          <td>
            % if len(desc.strip()) > 0:
              <div class="desc">${desc | mark}</div>
            % endif
          </td>
        </tr>
    % endfor
    </table>
% endif
</%def>

<%def name="show_column_list(items, numcols=3)">
  <%
    items = list(items)
    columns = [None] * numcols
    per = len(items) // numcols
    which_add1 = len(items) % numcols
    for c in range(numcols):
      numthis = per + 1 if c < which_add1 else per
      columns[c] = items[0:numthis]
      items = items[numthis:]
  %>
  <div class="column_list">
    % for column in columns:
      <ul>
        % for item in column:
          <li class="mono">${item}</li>
        % endfor
      </ul>
    % endfor
  </div>
</%def>

<%def name="show_module(module)">
  <%
    variables = module.variables()
    classes = module.classes()
    functions = module.functions()
    submodules = module.submodules()
  %>

  <%def name="show_func(f)">
    <div class="item">
      <h4 class="name def" id="${f.refname}">
        <p><span class="keyword">def</span> ${ident(f.name)}<span class="prams">(${f.spec() | h})</span></p>
      </h4>
      ${show_inheritance(f)}
      ${show_desc(f)}
    </div>
  </%def>

  % if 'http_server' in context.keys() and http_server:
      <p id="nav">
          <a href="/">All packages</a>
      <% parts = module.name.split('.')[:-1] %>
      % for i, m in enumerate(parts):
          <% parent = '.'.join(parts[:i+1]) %>
          :: <a href="/${parent.replace('.', '/')}">${parent}</a>
      % endfor
      </p>
  % endif

  <h1>${module.name}</h1>
  <!-- ${module.docstring | mark} -->
  ${show_source(module)}
  <hr>
  <script type="text/javascript">
    function toggle(id, $link) {
      $node = document.getElementById(id);
      if (!$node)
        return;
      if (!$node.style.display || $node.style.display == 'none') {
        $node.style.display = 'block';
        $link.innerHTML = 'Hide source.';
      } else {
        $node.style.display = 'none';
        $link.innerHTML = 'Show source.';
      }
    }
  </script>
  % if len(classes) > 0:
  <h2 id="header-classes">Classes</h2>
  % for c in classes:
      <%
        class_vars = c.class_variables()
        smethods = c.functions()
        inst_vars = c.instance_variables()
        methods = c.methods()
        mro = c.module.mro(c)
      %>
      <div class="item">
        <h3 id="${c.refname}" class="name">
          <span class="keyword">class</span> ${ident(c.name)}
        </h3>
        ${show_desc(c)}

        <div class="class">
          % if len(mro) > 1:
              <h4>Ancestors (in MRO)</h4>
              <ul class="class_list">
              % for cls in mro:
                <li>${link(cls.refname)}</li>
              % endfor
              </ul>
          % endif
          % if len(class_vars) > 0:
              <h4>Class variables</h4>
              % for v in class_vars:
                  <div class="item">
                    <p id="${v.refname}" class="name">
                      <span class="keyword">var</span> ${ident(v.name)}
                    </p>
                    ${show_inheritance(v)}
                    ${show_desc(v)}
                  </div>
              % endfor
          % endif
          % if len(smethods) > 0:
              <h4>Static methods</h4>
              % for f in smethods:
                  ${show_func(f)}
              % endfor
          % endif
          % if len(inst_vars) > 0:
              <h4>Instance variables</h4>
              % for v in inst_vars:
                  <div class="item">
                    <p id="${v.refname}" class="name">
                      <span class="keyword">var</span> ${ident(v.name)}
                    </p>
                    ${show_inheritance(v)}
                    ${show_desc(v)}
                  </div>
              % endfor
          % endif
          % if len(methods) > 0:
              <h4>Methods</h4>
              % for f in methods:
                  ${show_func(f)}
              % endfor
          % endif
        </div>
      </div>
  % endfor
  % endif

  % if len(submodules) > 0:
  <h2 id="header-submodules">Sub-modules</h2>
  % for m in submodules:
      <div class="item">
        <p class="name">${link(m.refname)}</p>
        ${show_desc(m, limit=300)}
      </div>
  % endfor
  % endif
</%def>


  % if module_list:
      <title>Python module list</title>
      <meta name="description" content="A list of Python modules in sys.path">
  % else:
      <title>${module.name} API documentation</title>
      <meta name="description" content="${module.docstring | glimpse, trim}">
  % endif

  <link href="/static/common/css/pdoc.css" rel="stylesheet">
  <!-- <%namespace name="css" file="css.mako" />
  <style type="text/css">
  ${css.pre()}
  </style>

  <style type="text/css">
  ${css.pdoc()}
  </style>
-->
<!--
  <style type="text/css">
  ${css.post()}
  </style>
-->

<div id="container">

<article id="content">
% if module_list:
    ${show_module_list(modules)}
% else:
    ${show_module(module)}
% endif
</article>
<hr>
</div>
