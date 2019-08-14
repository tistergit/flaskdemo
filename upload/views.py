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
    doc_version = request.values.get('doc_version','3.3.0')
    current_app.logger.info(doc_version)
    # photo是html中input的name
    if request.method == 'POST' and 'file' in request.files:
        # 将文件保存到本地
        # filename = photos.save(request.files['photo'])
        name = hashlib.md5(('admin' + str(time.time())).encode("utf8")).hexdigest()[:15]
        current_app.logger.info("name : " + name)
        filename = photos.save(request.files['file'], name=name+'.')

    return jsonify({'filename':filename}), 200

@bp.route('/mkdocs', methods=['POST', 'GET'])
def mkdocs():
    current_app.logger.info("values : " + str(request.json))
    p = Path("uploads/tmp/")
    p.mkdir(exist_ok=True)
    ###
    # with zipfile.ZipFile(request.files['file'], 'r') as zf:
    #     for fn in zf.namelist():
    #         dest_fn = "uploads/tmp/" + fn
    #         # current_app.logger.info("dest_fn : " + dest_fn)
    #         right_fn = dest_fn.encode('cp437').decode('utf8')  # 将文件名正确编码
    #         if right_fn.endswith("/"):
    #             if not os.path.exists(right_fn):
    #                 os.mkdir(right_fn)
    #         else:
    #             with open(right_fn, 'wb') as output_file:  # 创建并打开新文件
    #                 with zf.open(fn, 'r') as origin_file:  # 打开原文件
    #                     shutil.copyfileobj(origin_file, output_file)  # 将原文件内容复制到新文件
                        
            
    return jsonify({'filename':'filename'}), 200 

    # r = os.system("cd uploads/tmp;mkdocs build -d " + doc_version)
    # if r != 0:
    #     return "file upload error!!!",500

@bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('upload/index-vue.html')