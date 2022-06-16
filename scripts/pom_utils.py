from xml.dom.minidom import parse
import xml.dom.minidom


class PomModifier:

    def __init__(self, path):
        self._path = path
        self._dom = xml.dom.minidom.Document()
        self._tree = xml.dom.minidom.parse(path)
        self._root_ele = self._tree.documentElement

    def update_property(self, prop_name, prop_value):
        properties_ele = self._root_ele.getElementsByTagName("properties")[0]
        prop_ele_list = properties_ele.getElementsByTagName(prop_name)
        if prop_ele_list.length == 0:
            new_prop_ele = self._dom.createElement(prop_name)
            new_prop_node = self._dom.createTextNode(prop_value)
            new_prop_ele.appendChild(new_prop_node)
            properties_ele.appendChild(self._dom.createTextNode("\t"))
            properties_ele.appendChild(new_prop_ele)
            properties_ele.appendChild(self._dom.createTextNode("\r\n\t"))
        else:
            prop_ele = prop_ele_list[0]
            prop_node = prop_ele.childNodes[0]
            prop_node.data = prop_value

    def add_repository(self, repo_id, repo_url, release_enabled, release_update_policy, snapshot_enabled, snapshot_update_policy):
        repositories_node = self._root_ele.getElementsByTagName("repositories")

        id_ele = self._dom.createElement("id")
        id_node = self._dom.createTextNode(repo_id)
        id_ele.appendChild(id_node)

        url_ele = self._dom.createElement("url")
        url_node = self._dom.createTextNode(repo_url)
        url_ele.appendChild(url_node)

        release_enabled_ele = self._dom.createElement("enabled")
        release_enabled_node = self._dom.createTextNode(release_enabled)
        release_enabled_ele.appendChild(release_enabled_node)

        release_update_policy_ele = self._dom.createElement("updatePolicy")
        release_update_policy_node = self._dom.createTextNode(release_update_policy)
        release_update_policy_ele.appendChild(release_update_policy_node)

        release_ele = self._dom.createElement("releases")
        release_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t\t"))
        release_ele.appendChild(release_enabled_ele)
        release_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t\t"))
        release_ele.appendChild(release_update_policy_ele)
        release_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t"))

        snapshots_enabled_ele = self._dom.createElement("enabled")
        snapshots_enabled_node = self._dom.createTextNode(snapshot_enabled)
        snapshots_enabled_ele.appendChild(snapshots_enabled_node)

        snapshots_update_policy_ele = self._dom.createElement("updatePolicy")
        snapshots_update_policy_node = self._dom.createTextNode(snapshot_update_policy)
        snapshots_update_policy_ele.appendChild(snapshots_update_policy_node)

        snapshots_ele = self._dom.createElement("snapshots")
        snapshots_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t\t"))
        snapshots_ele.appendChild(snapshots_enabled_ele)
        snapshots_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t\t"))
        snapshots_ele.appendChild(snapshots_update_policy_ele)
        snapshots_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t"))

        cloudsmith_repo_ele = self._dom.createElement("repository")
        cloudsmith_repo_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t"))
        cloudsmith_repo_ele.appendChild(id_ele)
        cloudsmith_repo_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t"))
        cloudsmith_repo_ele.appendChild(url_ele)
        cloudsmith_repo_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t"))
        cloudsmith_repo_ele.appendChild(release_ele)
        cloudsmith_repo_ele.appendChild(self._dom.createTextNode("\r\n\t\t\t"))
        cloudsmith_repo_ele.appendChild(snapshots_ele)
        cloudsmith_repo_ele.appendChild(self._dom.createTextNode("\r\n\t\t"))

        repositories_node[0].childNodes.append(self._dom.createTextNode("\t"))
        repositories_node[0].childNodes.append(cloudsmith_repo_ele)
        repositories_node[0].childNodes.append(self._dom.createTextNode("\r\n\t"))

    def update_file(self, path=None):
        try:
            if path is None:
                path = self._path
            with open(path, 'w', encoding='UTF-8') as fh:
                # self._tree.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
                self._tree.writexml(fh)
                print('Success to update pom file')
        except Exception as err:
            print('Failed to update pom file：{err}'.format(err=err))


def test():
    modifier = PomModifier('../pom.xml')
    modifier.add_repository('staging', 'https://dl.cloudsmith.io/${env.CLOUDSMITH_API_KEY}/streamnative/staging/maven/', 'true', 'always', 'true', 'always')
    modifier.update_property('pulsar.version', '2.10.0xxxxxx')
    modifier.update_file('../test-pom.xml')
