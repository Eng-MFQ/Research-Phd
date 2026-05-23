# -*- coding: utf-8 -*-
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from APIs.AgenticIslam import AgenticIslam
from APIs.AhadeetAi import AhadeethAi
from APIs.NabilUsersApis import NabilUserApis

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
AgenticIslam(app)
AhadeethAi(app)
NabilUserApis(app)




# uvicorn main:app --reload
# problem with requirementsOld.txt check this.
# https://stackoverflow.com/questions/31684375/automatically-create-file-requirements-txt
# pip freeze > requirementsO.txt
# pip uninstall -r requirementsO.txt -y
# pip install -r requirementsO.txt
