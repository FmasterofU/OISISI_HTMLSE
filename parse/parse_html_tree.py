import os

from progressbar import progressbar

import structures
from parse.parser import Parser


def get_html_documents_list(top):
    """
    Returns paths of all html documents in specified directory's tree
    :param top: top directory path
    :return: list of paths of all html files in tree of top directory
    """

    ret = []
    if not os.path.isdir(top):
        print('Passed input is not a valid directory path. Reloading.')
        return None
    print('Getting directory tree and extracting all paths to HTML files...')
    for root, _, files in os.walk(top):
        for file in files:
            if '.htm' in file:  # takes .htm as well as .html documents
                ret.append(os.path.abspath(os.path.join(root, file)))
    print('Done.')
    return ret


class PopulateStructures:
    """
    Populate word trie tree and links graph from all HTML documents in a folder (complete directory tree).
    graph and trie are attributes of this class (instances of data structures implemented in structures package)
    """

    def __init__(self, top, ui_ux=True):
        self.graph = structures.Graph(directed=True)
        self.trie = structures.Trie()
        parser = Parser()
        # document = open('data.txt', mode='w', encoding='utf-8')
        self.html_files = get_html_documents_list(top)
        self.word_count = []
        if self.html_files is None:
            self.html_files = []
        elif len(self.html_files) == 0:
            print('No HTML files in given directory structure, reloading.')
        else:
            print('Populating trie and graph with data from all HTML files (total:{0})...'.format(len(self.html_files)))
            iterator_generator = progressbar(range(len(self.html_files))) if ui_ux else range(len(self.html_files))
            for i in iterator_generator:
                html_file = self.html_files[i]
                links, words = parser.parse(html_file)
                # document.write(str(html_file) + ' : ' + str(links) + ' ' + str(words) + '\n')
                self.word_count.append(len(words))
                self.graph.insert_vertex(html_file)
                for link in links:
                    self.graph.insert_vertex(link)
                    self.graph.insert_edge(html_file, link)
                for word in words:
                    self.trie.add_node(word, html_file)
            print("Trie and graph populated.")
