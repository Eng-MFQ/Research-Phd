from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: str = "user"
    content: str = "start"

    [
        {
            "role": "user",
            "content": "السلام عليكم"
        },
        {
            "role": "user",
            "content": "لم تعجبني إجابتك. أريد سؤال شيخ حقيقي."
        }
    ]


class RequestBodyLinkedin(BaseModel):
    messages: list[Message] = [
        {
            "role": "user",
            "content": " I want to join email list"
        },

    ]
    userId: str = "enas_ghazal__MgsPbKx15Q"
    clientName: Optional[str] = ""


class RequestBody(BaseModel):
    data: list[Message]


class Prompts(Enum):
    TOYS = 0
    WEAR = 1
    ZOO = 2
    EXPLORE = 3
    TRANSLATE = 4


class CondetionalAccess(Enum):
    FREE = 1234
    PRICED = 1235
    MAHARATECH = 1236


class VerifyBody(BaseModel):
    packageName: str = "com.whilelearn.kids.whilelearn_kids"
    productId: str = "buy_cridet_1_dollar"
    token: str
    source: Optional[str] = "google_play"


class Kids(BaseModel):
    userId: str = "105962983257369026275"
    langauge: str = "English"
    promptType: int = 0


class TextInputTranslate(BaseModel):
    tileToTranslate: str
    questionToTranslate: str
    answerToTranslate: str
    translateToLanguage: str = "English"


class TextInputFatwaId(BaseModel):
    fatwaQuestion: str = "كيف للإنسان يكون خاشعاً في صلاته أو ما هي الأعمال التي تجعلني أخشع؟"


class TextInputFatwaTitle(BaseModel):
    fatwaAnswer: str
    fatwaQuestion: str


class AgentixAiUser(BaseModel):
    email: Optional[str]
    userId: str = "UhRB0LFI2HR8GE05UVxVyh5ezXf2"
    photo: Optional[str] = None
    name: Optional[str] = None
    isSubscribed: Optional[bool] = False


class VoucherRequest(BaseModel):
    user_email: str
    agent_id: str


class EmailUser(BaseModel):
    name: str
    email: str


class AIAgentModel(BaseModel):
    ownerId: str = "muwaffaqimam@gmail.com"
    storeId: str = ""
    name: str
    systemInstructions: str
    color: Optional[str] = "#19ACE8"
    icon: Optional[str] = "📝"
    image: Optional[str]
    price: Optional[int]
    description: Optional[str]
    starter: Optional[list[str]] = ["Help me!"]
    threadInstructions: Optional[str]


class AIAssistantChatModel(BaseModel):
    threadId: str = "thread_yXwySRpVW6x48lUbjsfah0UG"
    assistantId: str = "asst_hABk3kLg7OGIbWUhrge6l3Ha"
    userMessage: str
    aiAgentId: Optional[str]
    userId: Optional[str]


class ContentGPT(BaseModel):
    userId: str = "muwaffaqimam@gmail.com"
    gptId: str = "wI-sBFytUY0znyslg9s8hdVI6wk"
    isDeepseek: bool = False


class Content(BaseModel):
    # userId: str = "muwaffaq_Imam-pvvetPFhldaoDQ"
    userId: str = ""
    prompt: str = ""
    promptType: int = 0


class ContentUser(BaseModel):
    # userId: str = "muwaffaq_Imam-pvvetPFhldaoDQ"
    userId: str = "muwaffaqimam@gmail.com"
    password: str
    name: Optional[str]


class ContentUrl(BaseModel):
    userId: str = ""
    url: str = ""
    language: str = "Arabic"
    withImage: bool = False


# class Query(BaseModel):
#     query: str
#     apiKey: str
#     userId: str


#
class Query(BaseModel):
    query: str = "Who is the founder?"
    apiKey: str = "okaymuk_VeryGood-JHyy8BwqAARRax9DU7_do1AjmvZs2TAjBJin_Px5O9k"
    userId: str = "105962983257369026275"


class Text(BaseModel):
    query: str


class Init(BaseModel):
    apiKey: str


class ExecutePayment(BaseModel):
    paymentId: str
    payerId: str
    userId: str
    sandbox: Optional[bool] = True


# class ExecutePayment(BaseModel):
#     paymentId: str = "PAYID-MVCRC5Y77779897K3659134K"
#     payerId: str = "WUCDM5CTS5LBJ"
#     userId: str = "105962983257369026275"
#     sandbox: Optional[bool] = True


class CreatePayment(BaseModel):
    amount: float
    redirectUrl: str
    sandbox: Optional[bool] = False
