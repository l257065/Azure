# -*- coding: utf-8 -*-
"""把已核對題目的答案區描述與解析小標對齊（#54 #137 #140 #192 #227）。
   #54 #137 #140 #192 是描述本身要照原文修；#227 是英文小標寫得與描述不同，改小標。
   一次性腳本，保留供追溯。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, arr

L = load()

# #54：原文的描述沒有引號，反推時多加了「」與 ''
patch(L, 54, None, line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦發生故障之後仍然保持可用的雲端服務⟧",
                             "⟦發生故障之後可以被復原的雲端服務⟧",
                             "⟦需求增加時仍能快速運作的雲端服務⟧",
                             "⟦可以從網際網路快速存取的雲端服務⟧"]) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦A cloud service that remains available after a failure occurs⟧",
                                     "⟦A cloud service that can be recovered after a failure occurs⟧",
                                     "⟦A cloud service that performs quickly when demand increases⟧",
                                     "⟦A cloud service that can be accessed quickly from the Internet⟧"]) + ','),
], text_subs=[
    ("【「發生故障之後仍然保持可用的雲端服務」】", "【發生故障之後仍然保持可用的雲端服務】"),
    ("【「發生故障之後可以被復原的雲端服務」】", "【發生故障之後可以被復原的雲端服務】"),
    ("【「需求增加時仍能快速運作的雲端服務」】", "【需求增加時仍能快速運作的雲端服務】"),
    ("【「可以從網際網路快速存取的雲端服務」】", "【可以從網際網路快速存取的雲端服務】"),
])

# #137：原文的三句都是大寫開頭（Executes code: / Is always stateful: / Runs only in the cloud:）
patch(L, 137, None, line_edits=[
    ("     tgt:[", '     tgt:' + arr(["⟦Executes code⟧", "⟦Is always stateful⟧", "⟦Runs only in the cloud⟧"]) + ','),
])

# #140 / #192：中文描述裡多補的（portable）（serverless code）與解析小標對不上，拿掉
CN_TGT = ["提供⟦作業系統⟧的虛擬化",
          "為虛擬化的應用程式提供⟦可攜⟧的執行環境",
          "是用來⟦建置、部署與擴縮網頁應用程式⟧的",
          "提供執行⟦無伺服器程式碼⟧的平台"]
patch(L, 140, None, line_edits=[(" tgt:[", ' tgt:' + arr(CN_TGT) + ',')])
patch(L, 192, None, line_edits=[
    (" tgt:[", ' tgt:' + arr(["提供⟦作業系統的虛擬化⟧",
                             "為虛擬化的應用程式提供⟦可攜⟧的執行環境",
                             "是用來⟦建置、部署⟧與擴縮網頁應用程式的",
                             "提供執行⟦無伺服器程式碼⟧的平台"]) + ',')])

# #227：英文小標與答案區描述寫法不同，把小標改成與描述一致
patch(L, 227, None, text_subs=[
    ("[Outermost: outside 'Identity and access']", "[The outermost layer, outside Identity & Access]"),
    ("[Between 'Identity and access' and 'Network']", "[Between Identity & Access and Network]"),
    ("[Between 'Compute' and 'Data']", "[Between Compute and Data]"),
])

save(L)
print("小標同步完成：#54 #137 #140 #192 #227")
