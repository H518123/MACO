# +
# encoding: utf-8
# -

import json
from xml.dom.minidom import Document
import os
import cv2


def readJson(jsonfile):
    with open(jsonfile,'r',encoding='utf-8') as f:
        jsonData = json.load(f)
    return jsonData


def getMinRect(points_coord):
    len_pts = len(points_coord)
    x_min = 10000
    y_min = 10000
    x_max = 0
    y_max = 0
    for i in range(len_pts):
        if points_coord[i][0] < x_min:
            x_min = points_coord[i][0]
        if points_coord[i][1] < y_min:
            y_min = points_coord[i][1]
        if points_coord[i][0] > x_max:
            x_max = points_coord[i][0]
        if points_coord[i][1] > y_max:
            y_max = points_coord[i][1]

    x_min, y_min, x_max, y_max = round(x_min), round(y_min), round(x_max), round(y_max)
    points = [str(x_min), str(y_min), str(x_max), str(y_max)]
    return points



def makexml(jsonPath, xmlPath, picPath, material_name):
    # 读取txt路径，xml保存路径，数据集图片所在路径
    files = os.listdir(picPath)
    for i, name in enumerate(files):
        xmlBuilder = Document()
        annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
        xmlBuilder.appendChild(annotation)
        img = cv2.imread(picPath + name[0:-4] + ".jpg")
        contentJson = readJson(jsonPath + name[0:-4] + ".json")
        Pheight, Pwidth, Pdepth = img.shape

        folder = xmlBuilder.createElement("folder")  # folder标签
        folderContent = xmlBuilder.createTextNode("&#38050;&#31563;&#22270;&#29255;")
        folder.appendChild(folderContent)
        annotation.appendChild(folder)

        filename = xmlBuilder.createElement("filename")  # filename标签
        filenameContent = xmlBuilder.createTextNode(name[0:-4])
        filename.appendChild(filenameContent)
        annotation.appendChild(filename)

        path = xmlBuilder.createElement("path")  # filename标签
        pathContent = xmlBuilder.createTextNode("D:/img/" + name[0:-4] + ".jpg")
        path.appendChild(pathContent)
        annotation.appendChild(path)

        source = xmlBuilder.createElement("source")
        datebase = xmlBuilder.createElement("database")
        databacecountent = xmlBuilder.createTextNode("Unknown")
        datebase.appendChild(databacecountent)
        source.appendChild(datebase)
        annotation.appendChild(source)

        size = xmlBuilder.createElement("size")  # size标签
        width = xmlBuilder.createElement("width")  # size子标签width
        widthContent = xmlBuilder.createTextNode(str(Pwidth))
        width.appendChild(widthContent)
        size.appendChild(width)
        height = xmlBuilder.createElement("height")  # size子标签height
        heightContent = xmlBuilder.createTextNode(str(Pheight))
        height.appendChild(heightContent)
        size.appendChild(height)
        depth = xmlBuilder.createElement("depth")  # size子标签depth
        depthContent = xmlBuilder.createTextNode(str(Pdepth))
        depth.appendChild(depthContent)
        size.appendChild(depth)
        annotation.appendChild(size)

        segment = xmlBuilder.createElement("segmented")
        segmentContent = xmlBuilder.createTextNode("0")
        segment.appendChild(segmentContent)
        annotation.appendChild(segment)

        for i in range(len(contentJson['shapes'])):
            txtList = getMinRect(contentJson['shapes'][i]["points"])


            object = xmlBuilder.createElement("object")
            type = xmlBuilder.createElement("type")
            typecoutent=xmlBuilder.createTextNode("bndbox")
            type.appendChild(typecoutent)
            object.appendChild(type)
            picname = xmlBuilder.createElement("name")
            nameContent = xmlBuilder.createTextNode(material_name)
            picname.appendChild(nameContent)
            object.appendChild(picname)
            pose = xmlBuilder.createElement("pose")
            poseContent = xmlBuilder.createTextNode("Unspecified")
            pose.appendChild(poseContent)
            object.appendChild(pose)
            truncated = xmlBuilder.createElement("truncated")
            truncatedContent = xmlBuilder.createTextNode("0")
            truncated.appendChild(truncatedContent)
            object.appendChild(truncated)
            difficult = xmlBuilder.createElement("difficult")
            difficultContent = xmlBuilder.createTextNode("0")
            difficult.appendChild(difficultContent)
            object.appendChild(difficult)
            rbndbox = xmlBuilder.createElement("bndbox")
            x = xmlBuilder.createElement("xmin")
            xContent = xmlBuilder.createTextNode(str(txtList[0]))
            x.appendChild(xContent)
            rbndbox.appendChild(x)
            y = xmlBuilder.createElement("ymin")
            y1Content = xmlBuilder.createTextNode(str(txtList[1]))
            y.appendChild(y1Content)
            rbndbox.appendChild(y)
            x = xmlBuilder.createElement("xmax")
            xContent = xmlBuilder.createTextNode(str(txtList[2]))
            x.appendChild(xContent)
            rbndbox.appendChild(x)
            y = xmlBuilder.createElement("ymax")
            yContent = xmlBuilder.createTextNode(str(txtList[3]))
            y.appendChild(yContent)
            rbndbox.appendChild(y)
            object.appendChild(rbndbox)

            annotation.appendChild(object)

            f = open(xmlPath + name[0:-4] + ".xml", 'w')
            xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
            f.close()


if __name__ == '__main__':
    jsons_dir = r"D:\json/"    # Path to JSON files for instance segmentation
    xmls_dir = r"D:\xml/"      # Path to the converted HBB annotation XML files
    imgs_dir = r"D:\img/"      # Path to the images
    material_name = "rebar"    # The class name of the material

    makexml(jsons_dir, xmls_dir, imgs_dir, material_name)
    print("ok!")

