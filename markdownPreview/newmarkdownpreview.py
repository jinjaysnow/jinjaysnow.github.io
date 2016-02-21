# -*- encoding: UTF-8 -*-
import cgi
import codecs
import json
import os
import re
import sys
import traceback


from urllib import pathname2url, url2pathname
from urlparse import urlparse, urlunparse

import markdown.extensions.codehilite as codehilite

from markdown_settings import Settings

from markdown_wrapper import StMarkdown as Markdown

from pygments.formatters import get_formatter_by_name

pygments_local = {
    'github': 'pygments_css/github.css',
    'github2014': 'pygments_css/github2014.css'
}

try:
    PYGMENTS_AVAILABLE = codehilite.pygments
except:
    PYGMENTS_AVAILABLE = False

unicode_str = unicode

_CANNOT_CONVERT = u'cannot convert markdown'

PATH_EXCLUDE = tuple(
    [
        'file://', 'https://', 'http://', '/', '#',
        "data:image/jpeg;base64,", "data:image/png;base64,", "data:image/gif;base64,"
    ] + ['\\'] if sys.platform.startswith('win') else []
)

ABS_EXCLUDE = tuple(
    [
        'file://', '/'
    ] + (['\\'] if sys.platform.startswith('win') else [])
)

DEFAULT_EXT = [
    "extra", "github", "toc",
    "meta", "sane_lists", "smarty", "wikilinks",
    "admonition"
]


def load_settings(filename):
    with open(filename) as f:
        fc = json.load(f)
    return fc


def getTempMarkdownPreviewPath(filename):
    ''' return a permanent full path of the temp markdown preview file '''
    # TODO: 文件路径
    return "../test.html"


def save_utf8(filename, text):
    with codecs.open(filename, 'w', encoding='utf-8')as f:
        f.write(text)


def load_utf8(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        return f.read()


def load_resource(filename):
    ''' return file contents for files within the package root folder '''
    # TODO: 文件名
    return load_utf8(filename)


def exists_resource(filename):
    # TODO: filename
    return os.path.isfile(filename)


def get_references(file_name, encoding="utf-8"):
    """ Get footnote and general references from outside source """
    text = ''
    if file_name is not None:
        if os.path.exists(file_name):
            try:
                with codecs.open(file_name, "r", encoding=encoding) as f:
                    text = f.read()
            except:
                print(traceback.format_exc())
        else:
            print("Could not find reference file %s!", file_name)
    return text


def parse_url(url):
    """
    Parse the url and
    try to determine if the following is a file path or
    (as we will call anything else) a url
    """

    RE_PATH = re.compile(r'file|[A-Za-z]')
    RE_WIN_DRIVE = re.compile(r"[A-Za-z]:?")
    RE_URL = re.compile('(http|ftp)s?|data|mailto|tel|news')
    is_url = False
    is_absolute = False
    scheme, netloc, path, params, query, fragment = urlparse(url)

    if RE_URL.match(scheme):
        # Clearly a url
        is_url = True
    elif scheme == '' and netloc == '' and path == '':
        # Maybe just a url fragment
        is_url = True
    elif scheme == '' or RE_PATH.match(scheme):
        if scheme not in ('', 'file') and netloc != '':
            # A non-nix filepath or strange url
            is_url = True
        else:
            # Check if nix path is absolute or not
            if path.startswith('/'):
                is_absolute = True
            scheme = ''
    return (scheme, netloc, path, params, query, fragment, is_url, is_absolute)


def repl_relative(m, base_path, relative_path):
    """ Replace path with relative path """

    RE_WIN_DRIVE_PATH = re.compile(r"(^(?P<drive>[A-Za-z]{1}):(?:\\|/))")
    link = m.group(0)
    try:
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = parse_url(m.group('path')[1:-1])

        if not is_url:
            # Get the absolute path of the file or return
            # if we can't resolve the path
            path = url2pathname(path)
            abs_path = None
            if (not is_absolute):
                # Convert current relative path to absolute
                temp = os.path.normpath(os.path.join(base_path, path))
                if os.path.exists(temp):
                    abs_path = temp.replace("\\", "/")
            elif os.path.exists(path):
                abs_path = path

            if abs_path is not None:
                # Determine if we should convert the relative path
                # (or see if we can realistically convert the path)
                convert = True

                # Convert the path, url encode it, and format it as a link
                if convert:
                    path = pathname2url(os.path.relpath(abs_path, relative_path).replace('\\', '/'))
                else:
                    path = pathname2url(abs_path)
                link = '%s"%s"' % (m.group('name'), urlunparse((scheme, netloc, path, params, query, fragment)))
    except:
        # Parsing crashed an burned; no need to continue.
        pass

    return link


def repl_absolute(m, base_path):
    """ Replace path with absolute path """
    link = m.group(0)

    try:
        scheme, netloc, path, params, query, fragment, is_url, is_absolute = parse_url(m.group('path')[1:-1])

        if (not is_absolute and not is_url):
            path = url2pathname(path)
            temp = os.path.normpath(os.path.join(base_path, path))
            if os.path.exists(temp):
                path = pathname2url(temp.replace("\\", "/"))
                link = '%s"%s"' % (m.group('name'), urlunparse((scheme, netloc, path, params, query, fragment)))
    except Exception:
        # Parsing crashed an burned; no need to continue.
        pass

    return link


class CriticDump(object):
    RE_CRITIC = re.compile(
        r'''
            ((?P<open>\{)
                (?:
                    (?P<ins_open>\+{2})(?P<ins_text>.*?)(?P<ins_close>\+{2})
                  | (?P<del_open>\-{2})(?P<del_text>.*?)(?P<del_close>\-{2})
                  | (?P<mark_open>\={2})(?P<mark_text>.*?)(?P<mark_close>\={2})
                  | (?P<comment>(?P<com_open>\>{2})(?P<com_text>.*?)(?P<com_close>\<{2}))
                  | (?P<sub_open>\~{2})(?P<sub_del_text>.*?)(?P<sub_mid>\~\>)(?P<sub_ins_text>.*?)(?P<sub_close>\~{2})
                )
            (?P<close>\})|.)
        ''',
        re.MULTILINE | re.DOTALL | re.VERBOSE
    )

    def process(self, m):
        if self.accept:
            if m.group('ins_open'):
                return m.group('ins_text')
            elif m.group('del_open'):
                return ''
            elif m.group('mark_open'):
                return m.group('mark_text')
            elif m.group('com_open'):
                return ''
            elif m.group('sub_open'):
                return m.group('sub_ins_text')
            else:
                return m.group(0)
        else:
            if m.group('ins_open'):
                return ''
            elif m.group('del_open'):
                return m.group('del_text')
            elif m.group('mark_open'):
                return m.group('mark_text')
            elif m.group('com_open'):
                return ''
            elif m.group('sub_open'):
                return m.group('sub_del_text')
            else:
                return m.group(0)

    def dump(self, source, accept):
        text = ''
        self.accept = accept
        for m in self.RE_CRITIC.finditer(source):
            text += self.process(m)
        return text


class MarkdownPreviewListener(object):
    ''' auto update the output html if markdown file has already been converted once '''
    # TODO: filename之前是view
    def on_post_save(self, filename):
        settings = load_settings('MarkdownPreview.sublime-settings')
        if settings.get('enable_autoreload', True):
            filetypes = settings.get('markdown_filetypes')
            if filetypes and filename.endswith(tuple(filetypes)):
                temp_file = getTempMarkdownPreviewPath(filename)
                if os.path.isfile(temp_file):
                    # reexec markdown conversion
                    # todo : check if browser still opened and reopen it if needed
                    from subprocess import call
                    call(["open", temp_file])


class Compiler(object):
    ''' Do the markdown converting '''
    default_css = "markdown.css"
    filename = "../first.md"
    html_template = None

    def __init__(self, file_name, html_template=None):
        self.filename = file_name

    def isurl(self, css_name):
        match = re.match(r'https?://', css_name)
        if match:
            return True
        return False

    def get_default_css(self):
        ''' locate the correct CSS with the 'css' setting '''
        css_name = self.settings.get('css', 'default')

        if self.isurl(css_name):
            # link to remote URL
            return u"<link href='%s' rel='stylesheet' type='text/css'>" % css_name
        elif os.path.isfile(os.path.expanduser(css_name)):
            # use custom CSS file
            return u"<style>%s</style>" % load_utf8(os.path.expanduser(css_name))
        elif css_name == 'default':
            # use parser CSS file
            return u"<style>%s</style>" % load_resource(self.default_css)

        return ''

    def get_override_css(self):
        ''' handls allow_css_overrides setting. '''

        if self.settings.get('allow_css_overrides'):
            filetypes = self.settings.get('markdown_filetypes')

            if self.filename and filetypes:
                for filetype in filetypes:
                    if self.filename.endswith(filetype):
                        css_filename = self.filename.rpartition(filetype)[0] + '.css'
                        if (os.path.isfile(css_filename)):
                            return u"<style>%s</style>" % load_utf8(css_filename)
        return ''

    def get_stylesheet(self):
        ''' return the correct CSS file based on parser and settings '''
        return self.get_default_css() + self.get_override_css()

    def get_javascript(self):
        js_files = self.settings.get('js')
        scripts = ''

        if js_files is not None:
            # Ensure string values become a list.
            if isinstance(js_files, str) or isinstance(js_files, unicode_str):
                js_files = [js_files]
            # Only load scripts if we have a list.
            if isinstance(js_files, list):
                for js_file in js_files:
                    if os.path.isabs(js_file):
                        # Load the script inline to avoid cross-origin.
                        scripts += u"<script>%s</script>" % load_utf8(js_file)
                    else:
                        scripts += u"<script type='text/javascript' src='%s'></script>" % js_file
        return scripts

    def get_mathjax(self):
        ''' return the MathJax script if enabled '''

        if self.settings.get('enable_mathjax') is True:
            return load_resource('mathjax.html')
        return ''

    def get_uml(self):
        ''' return the uml scripts if enabled '''

        if self.settings.get('enable_uml') is True:
            flow = load_resource('flowchart-min.js')
            return load_resource('uml.html').replace('{{ flowchart }}', flow, 1)
        return ''

    def get_highlight(self):
        return ''

    def get_contents(self, filename):
        ''' Get contents or selection from view and optionally strip the YAML front matter '''
        # TODO: 获取文件内容，从这里开始
        contents = load_resource(filename)

        # Remove yaml front matter
        if self.settings.get('strip_yaml_front_matter') and contents.startswith('---'):
            frontmatter, contents = self.preprocessor_yaml_frontmatter(contents)
            self.settings.apply_frontmatter(frontmatter)

        references = self.settings.get('builtin').get('references', [])
        for ref in references:
            contents += get_references(ref)

        contents = self.parser_specific_preprocess(contents)

        return contents

    def parser_specific_preprocess(self, text):
        return text

    def preprocessor_yaml_frontmatter(self, text):
        """ Get frontmatter from string """
        frontmatter = {}

        if text.startswith("---"):
            m = re.search(r'^(---(.*?)---\r?\n)', text, re.DOTALL)
            if m:
                try:
                    frontmatter = yaml.load(m.group(2))
                except:
                    print(traceback.format_exc())
                text = text[m.end(1):]

        return frontmatter, text

    def parser_specific_postprocess(self, text):
        return text

    def postprocessor_absolute(self, html, image_convert, file_convert):
        ''' fix relative paths in images, scripts, and links for the internal parser '''
        def tag_fix(m):
            tag = m.group('tag')
            src = m.group('src')
            if self.filename:
                # TODO: delete paltform = windows
                if (
                    not src.startswith(ABS_EXCLUDE) and
                    not (RE_WIN_DRIVE.match(src) is not None)
                ):
                    # Don't explicitly add file:// prefix,
                    # But don't remove them either
                    abs_path = u'%s/%s' % (os.path.dirname(self.filename), src)
                    # Don't replace just the first instance,
                    # but explicitly place it where it was before
                    # to ensure a file name 'img' dosen't replace
                    # the tag name etc.
                    if os.path.exists(abs_path):
                        tag = m.group('begin') + abs_path + m.group('end')
            return tag
        # Compile the appropriate regex to find images and/or files
        RE_WIN_DRIVE = re.compile(r"(^[A-Za-z]{1}:(?:\\|/))")
        RE_SOURCES = re.compile(
            r"""(?P<tag>(?P<begin><(?:%s%s%s)[^>]+(?:src%s)=["'])(?P<src>[^"']+)(?P<end>[^>]*>))""" % (
                r"img" if image_convert else "",
                r"|" if image_convert and file_convert else "",
                r"script|a" if file_convert else "",
                r"|href" if file_convert else ""
            )
        )
        return RE_SOURCES.sub(tag_fix, html)

    def postprocessor_pathconverter(self, html, image_convert, file_convert, absolute=False):

        RE_TAG_HTML = r'''(?xus)
        (?:
            (?P<comments>(\r?\n?\s*)<!--[\s\S]*?-->(\s*)(?=\r?\n)|<!--[\s\S]*?-->)|
            (?P<open><(?P<tag>(?:%s)))
            (?P<attr>(?:\s+[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)
            (?P<close>\s*(?:\/?)>)
        )
        '''

        RE_TAG_LINK_ATTR = re.compile(
            r'''(?xus)
            (?P<attr>
                (?:
                    (?P<name>\s+(?:href|src)\s*=\s*)
                    (?P<path>"[^"]*"|'[^']*')
                )
            )
            '''
        )

        RE_SOURCES = re.compile(
            RE_TAG_HTML % (
                (r"img" if image_convert else "") +
                (r"|" if image_convert and file_convert else "") +
                (r"script|a|link" if file_convert else "")
            )
        )

        def repl(m, base_path, rel_path=None):
            if m.group('comments'):
                tag = m.group('comments')
            else:
                tag = m.group('open')
                if rel_path is None:
                    tag += RE_TAG_LINK_ATTR.sub(lambda m2: repl_absolute(m2, base_path), m.group('attr'))
                else:
                    tag += RE_TAG_LINK_ATTR.sub(lambda m2: repl_relative(m2, base_path, rel_path), m.group('attr'))
                tag += m.group('close')
            return tag

        basepath = self.settings.get('builtin').get("basepath")
        if basepath is None:
            basepath = ""

        if absolute:
            if basepath:
                return RE_SOURCES.sub(lambda m: repl(m, basepath), html)
        else:
            if self.preview:
                relativepath = getTempMarkdownPreviewPath(self.view)
            else:
                relativepath = self.settings.get('builtin').get("destination")
                if not relativepath:
                    mdfile = self.view.file_name()
                    if mdfile is not None and os.path.exists(mdfile):
                        relativepath = os.path.splitext(mdfile)[0] + '.html'

            if relativepath:
                relativepath = os.path.dirname(relativepath)

            if basepath and relativepath:
                return RE_SOURCES.sub(lambda m: repl(m, basepath, relativepath), html)
        return html

    def postprocessor_base64(self, html):
        ''' convert resources (currently images only) to base64 '''

        file_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif"
        }

        exclusion_list = tuple(
            ['https://', 'http://', '#'] +
            ["data:%s;base64," % ft for ft in file_types.values()]
        )

        def b64(m):
            import base64
            src = m.group('src')
            data = m.group('tag')
            base_path = self.settings.get("basepath")
            if base_path is None:
                base_path = ""

            # Format the link
            absolute = False
            if src.startswith('file://'):
                src = src.replace('file://', '', 1)
                # if sublime.platform() == "windows" and not src.startswith('//'):
                #     src = src.lstrip("/")
                absolute = True
            # elif sublime.platform() == "windows" and RE_WIN_DRIVE.match(src) is not None:
            #     absolute = True

            # Make sure we are working with an absolute path
            if not src.startswith(exclusion_list):
                if absolute:
                    src = os.path.normpath(src)
                else:
                    src = os.path.normpath(os.path.join(base_path, src))

                if os.path.exists(src):
                    ext = os.path.splitext(src)[1].lower()
                    if ext in file_types:
                        try:
                            with open(src, "rb") as f:
                                data = m.group('begin') + "data:%s;base64,%s" % (
                                    file_types[ext],
                                    base64.b64encode(f.read()).decode('ascii')
                                ) + m.group('end')
                        except Exception:
                            pass
            return data
        RE_WIN_DRIVE = re.compile(r"(^[A-Za-z]{1}:(?:\\|/))")
        RE_SOURCES = re.compile(r"""(?P<tag>(?P<begin><(?:img)[^>]+(?:src)=["'])(?P<src>[^"']+)(?P<end>[^>]*>))""")
        return RE_SOURCES.sub(b64, html)

    def postprocessor_simple(self, html):
        ''' Strip out ids and classes for a simplified HTML output '''
        def strip_html(m):
            tag = m.group('open')
            if m.group('attr1'):
                tag += m.group('attr1')
            if m.group('attr2'):
                tag += m.group('attr2')
            if m.group('attr3'):
                tag += m.group('attr3')
            if m.group('attr4'):
                tag += m.group('attr4')
            if m.group('attr5'):
                tag += m.group('attr5')
            if m.group('attr6'):
                tag += m.group('attr6')
            tag += m.group('close')
            return tag

        # Strip out id, class and style attributes for a simple html output
        # Since we are stripping out two attributes, we need to set up the groups in such
        # a way so we can retrieve the data we don't want to throw away
        # up to these worst case scenarios:
        #
        # <tag attr=""... (id|class|style)=""... attr=""... (id|class|style)=""... attr=""... (id|class|style)=""...>
        # <tag (id|class|style)=""... attr=""... (id|class|style)=""... attr=""... (id|class|style)=""... attr=""...>
        STRIP_HTML = re.compile(
            r'''
                (?P<open><[\w\:\.\-]+)                                                      # Tag open
                (?:
                    (?P<attr1>(?:\s+(?!id|class|style)[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)  # Attributes to keep
                  | (?P<target1>\s+(?:id|class|style)(?:\s*=\s*(?:"[^"]*"|'[^']*'))*)             # Attributes to delte
                )
                (?:
                    (?P<attr2>(?:\s+(?!id|class|style)[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)  # Attributes to keep
                  | (?P<target2>\s+(?:id|class|style)(?:\s*=\s*(?:"[^"]*"|'[^']*'))*)             # Attributes to delte
                )?
                (?:
                    (?P<attr3>(?:\s+(?!id|class|style)[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)  # Attributes to keep
                  | (?P<target3>\s+(?:id|class|style)(?:\s*=\s*(?:"[^"]*"|'[^']*'))*)             # Attributes to delte
                )?
                (?:
                    (?P<attr4>(?:\s+(?!id|class|style)[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)  # Attributes to keep
                  | (?P<target4>\s+(?:id|class|style)(?:\s*=\s*(?:"[^"]*"|'[^']*'))*)             # Attributes to delte
                )?
                (?:
                    (?P<attr5>(?:\s+(?!id|class|style)[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)  # Attributes to keep
                  | (?P<target5>\s+(?:id|class|style)(?:\s*=\s*(?:"[^"]*"|'[^']*'))*)             # Attributes to delte
                )?
                (?:
                    (?P<attr6>(?:\s+(?!id|class|style)[\w\-:]+(?:\s*=\s*(?:"[^"]*"|'[^']*'))?)*)  # Attributes to keep
                  | (?P<target6>\s+(?:id|class|style)(?:\s*=\s*(?:"[^"]*"|'[^']*'))*)             # Attributes to delte
                )?
                (?P<close>\s*(?:\/?)>)                                                      # Tag end
            ''',
            re.MULTILINE | re.DOTALL | re.VERBOSE
        )
        return STRIP_HTML.sub(strip_html, html)

    def convert_markdown(self, markdown_text):
        ''' convert input markdown to HTML, with github or builtin parser '''

        markdown_html = self.parser_specific_convert(markdown_text)

        image_convert = self.settings.get("image_path_conversion", "absolute")
        file_convert = self.settings.get("file_path_conversions", "absolute")

        markdown_html = self.parser_specific_postprocess(markdown_html)

        if "absolute" in (image_convert, file_convert):
            markdown_html = self.postprocessor_pathconverter(markdown_html, image_convert, file_convert, True)

        if "relative" in (image_convert, file_convert):
            markdown_html = self.postprocessor_pathconverter(markdown_html, image_convert, file_convert, False)

        if image_convert == "base64":
            markdown_html = self.postprocessor_base64(markdown_html)

        if self.settings.get("html_simple", False):
            markdown_html = self.postprocessor_simple(markdown_html)

        return markdown_html

    def get_title(self):
        if self.meta_title is not None:
            title = self.meta_title
        else:
            title = self.filename

        # TODO: I changed here
        if not title:
            fn = self.filename
            title = 'untitled' if not fn else os.path.splitext(os.path.basename(fn))[0]
        return '<title>%s</title>' % cgi.escape(title)

    def get_meta(self):
        self.meta_title = None
        meta = []
        for k, v in self.settings.get("meta", {}).items():
            if k == "title":
                if isinstance(v, list):
                    if len(v) == 0:
                        v = ""
                    else:
                        v = v[0]
                self.meta_title = unicode_str(v)
                continue
            if isinstance(v, list):
                v = ','.join(v)
            if v is not None:
                meta.append(
                    '<meta name="%s" content="%s">' % (cgi.escape(k, True), cgi.escape(v, True))
                )
        return '\n'.join(meta)

# 主程序入口
    def run(self):
        ''' return full html and body html for view. '''
        self.settings = Settings('MarkdownPreview.sublime-settings', self.filename)

        contents = self.get_contents(self.filename)

        body = self.convert_markdown(contents)

        # add self.html_template, it can be assigned.
        if self.html_template is None:
            html_template = self.settings.get('html_template')
        else:
            html_template = self.html_template

        # use customized html template if given
        if self.settings.get('html_simple', False):
            html = body
        elif html_template and os.path.exists(html_template):
            head = u''
            head += self.get_meta()
            if not self.settings.get('skip_default_stylesheet'):
                head += self.get_stylesheet()
            head += self.get_javascript()
            head += self.get_highlight()
            head += self.get_mathjax()
            head += self.get_uml()
            head += self.get_title()

            html = load_utf8(html_template)
            html = html.replace('{{ HEAD }}', head, 1)
            html = html.replace('{{ BODY }}', body, 1)
        else:
            html = u'<!DOCTYPE html>'
            html += '<html><head><meta charset="utf-8">'
            html += self.get_meta()
            html += self.get_stylesheet()
            html += self.get_javascript()
            html += self.get_highlight()
            html += self.get_mathjax()
            html += self.get_title()
            html += '</head><body>'
            html += body
            html += '</body>'
            html += '</html>'

        return html, body


class MultiMarkdownCompiler(Compiler):
    default_css = "markdown.css"

    def parser_specific_convert(self, markdown_text):
        import subprocess
        binary = self.settings.get("multimarkdown_binary", "")
        if os.path.exists(binary):
            cmd = [binary]
            critic_mode = self.settings.get("strip_critic_marks", "accept")
            if critic_mode in ("accept", "reject"):
                cmd.append('-a' if critic_mode == "accept" else '-r')
            print('converting markdown with multimarkdown...')
            p = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            for line in markdown_text.split('\n'):
                p.stdin.write((line + '\n').encode('utf-8'))
            markdown_html = p.communicate()[0].decode("utf-8")
            if p.returncode:
                # Log info to console
                print("Could not convert file! See console for more info.")
                print(markdown_html)
                markdown_html = _CANNOT_CONVERT
        else:
            print("Cannot find multimarkdown binary!")
            markdown_html = _CANNOT_CONVERT
        return markdown_html


class MarkdownCompiler(Compiler):
    default_css = "markdown.css"

    def set_highlight(self, pygments_style, css_class):
        ''' Set the Pygments css. '''

        if pygments_style and not self.noclasses:
            style = None
            if pygments_style not in pygments_local:
                try:
                    style = get_formatter_by_name('html', style=pygments_style).get_style_defs('.codehilite pre')
                except Exception:
                    pygments_style = 'github'

            if style is None:
                style = load_resource(pygments_local[pygments_style]) % {
                    'css_class': ''.join(['.' + x for x in css_class.split(' ') if x])
                }

            self.pygments_style = '<style>%s</style>' % style
        return pygments_style

    def get_highlight(self):
        ''' return the Pygments css if enabled. '''
        return self.pygments_style if self.pygments_style else ''

        # highlight = ''
        # if self.pygments_style and not self.noclasses:
        #     highlight += '<style>%s</style>' % HtmlFormatter(style=self.pygments_style).get_style_defs('.codehilite pre')

        # return highlight

    def preprocessor_critic(self, text):
        ''' Stip out multi-markdown critic marks.  Accept changes by default '''
        return CriticDump().dump(text, self.settings.get("strip_critic_marks", "accept") == "accept")

    def parser_specific_preprocess(self, text):
        if self.settings.get("strip_critic_marks", "accept") in ["accept", "reject"]:
            text = self.preprocessor_critic(text)
        return text

    def process_extensions(self, extensions):
        re_pygments = re.compile(r"(?:\s*,)?pygments_style\s*=\s*([a-zA-Z][a-zA-Z_\d]*)")
        re_pygments_replace = re.compile(r"pygments_style\s*=\s*([a-zA-Z][a-zA-Z_\d]*)")
        re_use_pygments = re.compile(r"use_pygments\s*=\s*(True|False)")
        re_insert_pygment = re.compile(r"(?P<bracket_start>codehilite\([^)]+?)(?P<bracket_end>\s*\)$)|(?P<start>codehilite)")
        re_no_classes = re.compile(r"(?:\s*,)?noclasses\s*=\s*(True|False)")
        re_css_class = re.compile(r"css_class\s*=\s*([\w\-]+)")
        # First search if pygments has manually been set,
        # and if so, read what the desired color scheme to use is
        self.pygments_style = None
        self.noclasses = False
        use_pygments = True
        pygments_css = None

        count = 0
        for e in extensions:
            if e.startswith("codehilite"):
                m = re_use_pygments.search(e)
                use_pygments = True if m is None else m.group(1) == 'True'
                m = re_css_class.search(e)
                css_class = m.group(1) if m else 'codehilite'
                pygments_style = re_pygments.search(e)
                if pygments_style is None:
                    pygments_style = "github"
                    m = re_insert_pygment.match(e)
                    if m is not None:
                        if m.group('bracket_start'):
                            start = m.group('bracket_start') + ',pygments_style='
                            end = ")"
                        else:
                            start = m.group('start') + "(pygments_style="
                            end = ')'

                        extensions[count] = start + pygments_style + end
                else:
                    pygments_style = pygments_style.group(1)

                # Set the style, but erase the setting if the CSS is pygments_local.
                # Don't allow 'no_css' with non internal themes.
                # Replace the setting with the correct name if the style was invalid.
                original = pygments_css
                pygments_css = self.set_highlight(pygments_style, css_class)
                if pygments_css in pygments_local:
                    extensions[count] = re_no_classes.sub('', re_pygments.sub('', e))
                elif original != pygments_css:
                    extensions[count] = re_pygments_replace.sub('pygments_style=%s' % pygments_css, e)

                noclasses = re_no_classes.search(e)
                if noclasses is not None and noclasses.group(1) == "True":
                    self.noclasses = True
            count += 1

        # Second, if nothing manual was set, see if "enable_highlight" is enabled with pygment support
        # If no style has been set, setup the default
        if (
            pygments_css is None and
            self.settings.get("enable_highlight") is True
        ):
            pygments_css = self.set_highlight('github', 'codehilite')
            guess_lang = str(bool(self.settings.get("guess_language", True)))
            use_pygments = bool(self.settings.get("enable_pygments", True))
            extensions.append(
                "codehilite(guess_lang=%s,use_pygments=%s)" % (
                    guess_lang, str(use_pygments)
                )
            )

        if not use_pygments:
            self.pygments_style = None

        # Get the base path of source file if available
        base_path = self.settings.get("basepath")
        if base_path is None:
            base_path = ""

        # Replace BASE_PATH keyword with the actual base_path
        return [e.replace("${BASE_PATH}", base_path) for e in extensions]

    def get_config_extensions(self, default_extensions):
        config_extensions = self.settings.get('enabled_extensions')
        if not config_extensions or config_extensions == 'default':
            return self.process_extensions(default_extensions)
        if 'default' in config_extensions:
            config_extensions.remove('default')
            config_extensions.extend(default_extensions)
        return self.process_extensions(config_extensions)

    def parser_specific_convert(self, markdown_text):
        print('converting markdown with Python markdown...')
        config_extensions = self.get_config_extensions(DEFAULT_EXT)
        md = Markdown(extensions=config_extensions)
        html_text = md.convert(markdown_text)
        # Retrieve the meta data returned from the "meta" extension
        self.settings.add_meta(md.Meta)
        return html_text


# mdc = MarkdownCompiler("../blog/dict.md")
# html, body = mdc.run()
# print html
