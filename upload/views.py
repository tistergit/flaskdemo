#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by Flynn on 2018-08-29 18:12


from flask import Blueprint, request, render_template,jsonify
from flask_uploads import UploadSet, IMAGES,DEFAULTS,ARCHIVES
import logging
from flask import current_app
import flask_uploads
import time
import hashlib
import os
from pathlib import Path
import zipfile,shutil


bp = Blueprint('upload', __name__, url_prefix='/upload2/')

# photos是UploadSet的名字，这个名字将在配置中使用
# 第二个参数表示可上传文件类型，例如TEXT,DOCUMENTS,IMAGES
#photos = UploadSet('photos',extensions=('txt', 'rtf', 'odf', 'ods', 'gnumeric', 'abw', 'doc', 'docx', 'xls', 'xlsx', 'jpg', 'jpe', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'csv', 'ini', 'json', 'plist', 'xml', 'yaml', 'yml' , 'pdf','md','zip'))
photos = UploadSet('photos',DEFAULTS + ARCHIVES)



@bp.route('/file_upload', methods=['POST', 'GET'])
def file_upload():
    # print(request.files)
    current_app.logger.info(request.files)
    current_app.logger.info(request.values)
    upload_file = []
    # photo是html中input的name
    if request.method == 'POST' and 'file' in request.files:
        # 将文件保存到本地
        # filename = photos.save(request.files['photo'])
        name = hashlib.md5(('admin' + str(time.time())).encode("utf8")).hexdigest()[:15]
        current_app.logger.info("name : " + name)
        filename = photos.save(request.files['file'], name=name+'.')
        upload_file.append(filename)
    return jsonify({'upload_file':upload_file}), 200


@bp.route('/mkdocs', methods=['POST', 'GET'])
def mkdocs():
    current_app.logger.info("values : " + str(request.json))
    p = Path("uploads/tmp/")
    p.mkdir(exist_ok=True)
    data = request.get_json()
    current_app.logger.info("data : " + str(data))
    upload_files = data["upload_files"]
    doc_version = data.get("doc_version")
    current_app.logger.info("upload_files : " + str(upload_files))
    ###
    zip_filename = ''
    yml_filename = ''
    for a_file in upload_files:
        if "zip" in a_file[0]:
            zip_filename = a_file[0]
        if "yml" in a_file[0]:
            yml_filename = a_file[0]
    current_app.logger.info("zip_file : " + zip_filename )
    current_app.logger.info(" yml_filename : " + yml_filename)
    with zipfile.ZipFile("uploads/" + zip_filename, 'r') as zf:
        for fn in zf.namelist():
            dest_fn = "uploads/tmp/" + fn
            # current_app.logger.info("dest_fn : " + dest_fn)
            right_fn = dest_fn.encode('cp437').decode('utf8')  # 将文件名正确编码
            if right_fn.endswith("/"):
                if not os.path.exists(right_fn):
                    os.mkdir(right_fn)
            else:
                with open(right_fn, 'wb') as output_file:  # 创建并打开新文件
                    with zf.open(fn, 'r') as origin_file:  # 打开原文件
                        shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件
    from shutil import copyfile
    copyfile("uploads/" + yml_filename, "uploads/tmp/" + yml_filename)
    build_cmd = "cd uploads/tmp;mkdocs build -q -c -d " + doc_version + " -f " + yml_filename
    current_app.logger.info("build_cmd : " + build_cmd)
    r = os.system(build_cmd)
    r = 0 
    if r != 0:
        return u"构建失败!!!",500                        
    return jsonify({'message':'构建成功!!!','code':'200'}), 200      
    # return jsonify({'filename':'filename'}), 200 



@bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('upload/index-vue.html')