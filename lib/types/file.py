from lib.types.group import BasicGroupData


class FileInfo:
    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        self.path = data["path"]
        parentFolder = data["parent"]
        self.parentFolder = FolderInfo(parentFolder) if parentFolder is not None else "/"
        self.groupInfo = BasicGroupData(data["contact"])
        self.size = data["size"]
        self.uploaderId = data["uploaderId"]
        self.uploadTime = data["uploadTime"]
        self.lastModifyTime = data["lastModifyTime"]
        self.sha1 = data["sha1"]
        self.md5 = data["md5"]
        self.downloadTimes = data["downloadInfo"]["downloadTimes"] if data["downloadInfo"] is not None else None
        self.url = data["downloadInfo"]["url"] if data["downloadInfo"] is not None else None


class FolderInfo:
    def __init__(self, data):
        self.name = data["name"]
        self.id = data["id"]
        self.path = data["path"]
        parentFolder = data["parent"]
        self.parentFolder = FolderInfo(parentFolder) if parentFolder is not None else "/"
        self.groupInfo = BasicGroupData(data["contact"])
