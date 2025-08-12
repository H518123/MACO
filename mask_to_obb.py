# +
# encoding: utf-8
# -

import json
from xml.dom.minidom import Document
import os
import cv2
import numpy as np
import math


def readJson(jsonfile):
    with open(jsonfile, 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
    return jsonData


def getMinObbRect(points_coord):
    points = np.intp(points_coord)
    rect = cv2.minAreaRect(points)
    box = np.intp(cv2.boxPoints(rect))
    x1, y1, x2, y2 = box[1][0], box[1][1], box[2][0], box[2][1]
    cx, cy, w, h = rect[0][0], rect[0][1], rect[1][0], rect[1][1]
    angle = math.atan2(y2-y1, x2-x1)
    points = [str(cx), str(cy), str(w), str(h), str(angle)]
    return points


def makexml(jsonPath, xmlPath, picPath, material_name):
    # 读取txt路径，xml保存路径，数据集图片所在路径
    files = os.listdir(picPath)
    for i, name in enumerate(files):
        try:
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
                txtList = getMinObbRect(contentJson['shapes'][i]["points"])

                object = xmlBuilder.createElement("object")
                type = xmlBuilder.createElement("type")
                typecoutent=xmlBuilder.createTextNode("robndbox")
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
                rbndbox = xmlBuilder.createElement("robndbox")
                x = xmlBuilder.createElement("cx")
                xContent = xmlBuilder.createTextNode(str(txtList[0]))
                x.appendChild(xContent)
                rbndbox.appendChild(x)
                y = xmlBuilder.createElement("cy")
                y1Content = xmlBuilder.createTextNode(str(txtList[1]))
                y.appendChild(y1Content)
                rbndbox.appendChild(y)
                w = xmlBuilder.createElement("w")
                wContent = xmlBuilder.createTextNode(str(txtList[2]))
                w.appendChild(wContent)
                rbndbox.appendChild(w)
                h = xmlBuilder.createElement("h")
                hContent = xmlBuilder.createTextNode(str(txtList[3]))
                h.appendChild(hContent)
                rbndbox.appendChild(h)
                angle = xmlBuilder.createElement("angle")
                angleContent = xmlBuilder.createTextNode(str(txtList[4]))
                angle.appendChild(angleContent)
                rbndbox.appendChild(angle)

                object.appendChild(rbndbox)

                annotation.appendChild(object)

                f = open(xmlPath + name[0:-4] + ".xml", 'w')
                xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
                f.close()
        except:
            print(name + " is wrong!")


if __name__ == '__main__':
    jsons_dir = r"D:\json/"    # Path to JSON files for instance segmentation
    xmls_dir = r"D:\xml/"      # Path to the converted OBB annotation XML files
    imgs_dir = r"D:\img/"      # Path to the images
    material_name = "rebar"    # The class name of the material

    makexml(jsons_dir, xmls_dir, imgs_dir, material_name)
    print("ok!")

