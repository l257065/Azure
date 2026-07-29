# -*- coding: utf-8 -*-
"""核對原文 批次 C：#149 #150 #161 #162 #169 #170 #171（PDF 第 45、48、50、51 頁）。
   同時把解析改寫成「共用對照一次 + 逐格重點」。一次性腳本，保留供追溯。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, js, arr, arr2

L = load()

SVC_SHARE = """三種雲端服務模型的責任分界，一次列清楚（由你管得多排到管得少）：
・⟦基礎結構即服務（IaaS）⟧— 雲端商只負責實體資料中心、實體網路、實體主機與虛擬化層。作業系統、修補、防火牆設定、中介軟體、執行階段、應用程式與資料全部歸你。代表：Azure 虛擬機器、虛擬網路、受控磁碟。
・⟦平台即服務（PaaS）⟧— 雲端商多接手作業系統、修補與執行階段，你只管應用程式與資料。代表：Azure App Service、Azure SQL Database、Azure Functions。
・⟦軟體即服務（SaaS）⟧— 連應用程式本身都由雲端商提供與維運，你只管自己的資料、帳號與存取設定。代表：Microsoft 365、Dynamics 365、Outlook.com。
三個模型都一樣的兩端：⟦資料、裝置、帳戶與身分永遠歸你；實體主機、實體網路、實體資料中心永遠歸雲端商⟧。差別只在中間那幾層誰管。"""

SVC_SHARE_EN = """The responsibility split across the three cloud service models, laid out once (most yours to least):
・⟦Infrastructure as a service (IaaS)⟧ — the provider covers the physical datacenter, physical network, physical hosts and the virtualization layer. The OS, patching, firewall configuration, middleware, runtime, application and data are all yours. Examples: Azure virtual machines, virtual networks, managed disks.
・⟦Platform as a service (PaaS)⟧ — the provider also takes the OS, patching and runtime; you keep the application and its data. Examples: Azure App Service, Azure SQL Database, Azure Functions.
・⟦Software as a service (SaaS)⟧ — the application itself is delivered and operated by the provider; you keep only your data, accounts and access settings. Examples: Microsoft 365, Dynamics 365, Outlook.com.
The two ends never move: ⟦data, devices, accounts and identities are always yours; physical hosts, physical network and physical datacenter are always the provider's⟧. Only the layers in between change hands."""

# ══ #149（PDF 第 45 頁）══════════════════════════════════════════════
E149 = SVC_SHARE + """

【Azure App Service】→ 平台即服務（PaaS）
App Service 是託管網頁應用程式的平台：你部署程式碼，平台負責作業系統修補、執行階段更新、負載平衡與自動調整規模。你碰不到底下的虛擬機器，所以不是 IaaS；它也不是一套現成可用的商業軟體，所以不是 SaaS。

【Azure 虛擬機器】→ 基礎結構即服務（IaaS）
拿到的是一台完整的機器：作業系統、修補、防毒、上面裝什麼全是你的事。這是 IaaS 的標準代表。

【Microsoft Dynamics 365】→ 軟體即服務（SaaS）
Dynamics 365 是現成的 CRM／ERP 應用程式，開帳號登入就能用，不必部署也不必維護。與 Microsoft 365、Outlook.com 同一類。"""

EN149 = SVC_SHARE_EN + """

[Azure App Service] -> Platform as a service (PaaS)
App Service is a hosting platform for web apps: you deploy code and the platform handles OS patching, runtime updates, load balancing and autoscale. You never touch the virtual machines underneath, so it is not IaaS; nor is it a finished business application, so it is not SaaS.

[Azure virtual machines] -> Infrastructure as a service (IaaS)
What you get is a whole machine — OS, patching, antivirus and whatever you install on it are all your problem. The textbook example of IaaS.

[Microsoft Dynamics 365] -> Software as a service (SaaS)
Dynamics 365 is a finished CRM/ERP application: create an account, sign in, use it. Nothing to deploy and nothing to maintain, in the same family as Microsoft 365 and Outlook.com."""

patch(L, 149, """Question #149  ·  Topic 1  ·  DRAG DROP
Match the cloud service models to the appropriate offerings.
To answer, drag the appropriate model from the column on the left to its offering on the right. Each model may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Models：Infrastructure as a service (IaaS) ｜ Platform as a service (PaaS) ｜ Software as a service (SaaS)

Answer Area（紅框標出的正解順序）
1. Azure App Service　→　Platform as a service (PaaS)
2. Azure virtual machines　→　Infrastructure as a service (IaaS)
3. Microsoft Dynamics 365　→　Software as a service (SaaS)

（核對來源：PDF 第 45 頁）""", line_edits=[
    (" e:", ' e:' + js(E149) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Azure App Service⟧", "⟦Azure virtual machines⟧", "⟦Microsoft Dynamics 365⟧"]) + ','),
    ("     e:", '     e:' + js(EN149) + '}},'),
])

# ══ #150（PDF 第 45 頁）══════════════════════════════════════════════
E150 = """一樣是 IaaS / PaaS / SaaS 三選一，但這一題給的是「解決方案的描述」而不是服務名稱，判斷方式是問「作業系統歸誰管、應用程式誰寫」：
・⟦基礎結構即服務（IaaS）⟧— 你拿到虛擬機器，作業系統與上面跑的東西都自己管。描述裡出現「伺服器」通常就是它。
・⟦平台即服務（PaaS）⟧— 平台給你執行環境，你部署自己寫的應用程式，不必管作業系統。描述裡出現「自訂應用程式」「開發人員」通常就是它。
・⟦軟體即服務（SaaS）⟧— 現成的商業應用程式，訂閱就能用。描述裡出現「會計系統」「CRM」「電子郵件」這類成品就是它。
不變的兩端：⟦資料、裝置、帳戶與身分永遠歸你；實體主機、實體網路、實體資料中心永遠歸雲端商⟧。

【雲端上的檔案伺服器】→ 基礎結構即服務（IaaS）
關鍵字是「伺服器」。在雲端開一台檔案伺服器，等於開一台虛擬機器再自己裝檔案服務，作業系統歸你管。
注意一個容易混淆的地方：⟦如果題目說的是「Azure 檔案共用（Azure Files）」而不是「檔案伺服器」，那就偏向 PaaS⟧，因為 Azure Files 是完全受控的服務，沒有作業系統要你管。這兩個說法在考題裡是不同的東西，要看清楚字面。

【雲端上的會計系統】→ 軟體即服務（SaaS）
會計系統是現成的商業應用程式，訂閱後直接使用，不必自己開發也不必維運。

【供自訂應用程式使用的雲端服務】→ 平台即服務（PaaS）
關鍵字是「自訂應用程式」。你要自己寫程式，但不想管作業系統，那就是 PaaS。"""

EN150 = """Again it is IaaS / PaaS / SaaS, but this time the boxes describe solutions rather than naming services. Ask who owns the operating system and who writes the application:
・⟦Infrastructure as a service (IaaS)⟧ — you get virtual machines and own the OS and everything on it. The word 'server' in a description usually points here.
・⟦Platform as a service (PaaS)⟧ — the platform gives you a runtime and you deploy your own application, with no OS to manage. 'Custom apps' or 'developers' usually point here.
・⟦Software as a service (SaaS)⟧ — a finished business application you subscribe to. 'Accounting system', 'CRM' or 'email' point here.
The fixed ends: ⟦data, devices, accounts and identities are always yours; physical hosts, physical network and physical datacenter are always the provider's⟧.

[A cloud-based file server] -> Infrastructure-as-a-Service (IaaS)
The key word is 'server'. Standing up a file server in the cloud means standing up a virtual machine and installing the file service yourself, so the OS is yours.
One trap worth noting: ⟦if the question says 'Azure Files' rather than 'file server', the answer leans PaaS⟧, because Azure Files is a fully managed service with no OS for you to manage. Exam questions treat the two phrasings as different things, so read the wording closely.

[A cloud-based accounting system] -> Software-as-a-Service (SaaS)
An accounting system is a finished business application: subscribe and use it, with nothing to build and nothing to operate.

[A cloud-based service for custom apps] -> Platform-as-a-Service (PaaS)
The key phrase is 'custom apps'. You write the code but do not want the operating system — that is PaaS."""

patch(L, 150, """Question #150  ·  Topic 1  ·  DRAG DROP
Match the cloud service models to the appropriate solutions.
To answer, drag the appropriate cloud service model from the column on the left to its solution on the right Each cloud service model may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

（可拖曳欄）：Infrastructure-as-a-Service (IaaS) ｜ Platform-as-a-Service (PaaS) ｜ Software-as-a-Service (SaaS)

Answer Area（紅框標出的正解順序）
1. A cloud-based file server　→　Infrastructure-as-a-Service (IaaS)
2. A cloud-based accounting system　→　Software-as-a-Service (SaaS)
3. A cloud-based service for custom apps　→　Platform-as-a-Service (PaaS)

（核對來源：PDF 第 45 頁）""", line_edits=[
    (" e:", ' e:' + js(E150) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦A cloud-based file server⟧", "⟦A cloud-based accounting system⟧", "⟦A cloud-based service for custom apps⟧"]) + ','),
    ("     e:", '     e:' + js(EN150) + '}},'),
])

# ══ #161（PDF 第 48 頁）══════════════════════════════════════════════
# 原文第一格的選項順序是 admin. / portal. / www.，反推版本把 portal 排到第一個。
E161 = """Azure 入口網站的網址是 ⟦https://portal.azure.com⟧，這是唯一能管理所有 Azure 資源的入口。題目裡的「10 個網頁應用程式」是干擾——不管環境裡有什麼資源，管理入口都是同一個。
幾個容易混淆的網域一起記：
・⟦portal.azure.com⟧— Azure 入口網站，管理所有 Azure 資源。
・⟦azurewebsites.net⟧— App Service 網頁應用程式的預設網域（例如 myapp.azurewebsites.net）。那是應用程式本身的網址，不是管理介面。
・⟦azure.microsoft.com⟧— Azure 的公開產品與文件網站，不能拿來管理資源。
・⟦admin.microsoft.com⟧— Microsoft 365 系統管理中心，管的是 M365 租用戶，不是 Azure 資源。
・⟦entra.microsoft.com⟧— Microsoft Entra 系統管理中心，只管身分與存取。
・⟦shell.azure.com⟧— 只有 Cloud Shell 的網頁版。

【第 1 格】→ portal
管理介面用 portal。admin 是 Microsoft 365 的管理中心，www 則什麼也不是。

【第 2 格】→ azure
組起來就是 portal.azure.com。選 azurewebsites 會變成應用程式自己的網域，選 microsoft 會變成產品介紹網站。"""

EN161 = """The Azure portal lives at ⟦https://portal.azure.com⟧, and it is the one place from which every Azure resource can be managed. The '10 web apps' in the stem are a distraction — whatever the environment contains, the management entry point is the same.
Keep the easily confused domains apart:
・⟦portal.azure.com⟧ — the Azure portal, for managing all Azure resources.
・⟦azurewebsites.net⟧ — the default domain for App Service web apps (myapp.azurewebsites.net). That is the application's own address, not a management interface.
・⟦azure.microsoft.com⟧ — Azure's public product and documentation site; nothing can be managed there.
・⟦admin.microsoft.com⟧ — the Microsoft 365 admin center, which governs an M365 tenant, not Azure resources.
・⟦entra.microsoft.com⟧ — the Microsoft Entra admin center, identity and access only.
・⟦shell.azure.com⟧ — Cloud Shell on its own.

[Blank 1] -> portal
Management uses portal. 'admin' is the Microsoft 365 admin center and 'www' is nothing at all.

[Blank 2] -> azure
Together they spell portal.azure.com. 'azurewebsites' would give the application's own domain and 'microsoft' the marketing site."""

patch(L, 161, """Question #161  ·  Topic 1  ·  HOTSPOT
You have an Azure environment that contains 10 web apps. To which URL should you connect to manage all the Azure resources? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.
Hot Area:

Answer Area
https://　▼　admin. ｜ portal. ｜ www.　　▼　azure. ｜ azurewebsites. ｜ microsoft.　com

紅框標出的正解
1. 第 1 格　→　portal.
2. 第 2 格　→　azure.

（核對來源：PDF 第 48 頁）""", line_edits=[
    (" dd:[", ' dd:' + arr2([["admin", "portal", "www"], ["azure", "azurewebsites", "microsoft"]]) + ','),
    (" a:[", ' a:[1,0],'),
    (" e:", ' e:' + js(E161) + ','),
    ("     dd:[", '     dd:' + arr2([["admin", "portal", "www"], ["azure", "azurewebsites", "microsoft"]]) + ','),
    ("     e:", '     e:' + js(EN161) + '}},'),
])

# ══ #162（PDF 第 48 頁）══════════════════════════════════════════════
E162 = """題目要的是「備援程度由低到高」，答案是 ⟦LRS → ZRS → GRS⟧。六種儲存體備援選項一次列全（複本數／擋得住什麼）：
・⟦本地備援儲存體（LRS）⟧— 3 份複本，全部放在同一個資料中心的單一實體位置。擋得住磁碟、伺服器、機架故障；擋不住整個資料中心失效。年度耐久性 11 個 9，最便宜。
・⟦區域備援儲存體（ZRS）⟧— 3 份複本，分散在同一個區域內的三個可用性區域。擋得住整個資料中心失效；擋不住整個區域的災害。12 個 9。
・⟦異地備援儲存體（GRS）⟧— 主要區域內先做 LRS（3 份），再非同步複寫到數百公里外的配對次要區域也做 LRS（3 份），共 6 份。擋得住整個區域的災害。16 個 9。次要區域平時不可讀。
・⟦讀取權限異地備援儲存體（RA-GRS）⟧— GRS 再加上「次要區域可以直接讀」。
・⟦異地區域備援儲存體（GZRS）⟧— 主要區域用 ZRS（跨三個可用性區域）＋次要區域用 LRS，同時擋資料中心與區域，最完整。
・⟦讀取權限異地區域備援儲存體（RA-GZRS）⟧— GZRS 再加上次要區域可讀。
排序的邏輯是⟦擋的範圍越大就越備援⟧：LRS 擋到機架、ZRS 擋到資料中心、GRS 擋到整個區域，一路往外擴。

【第 1 個：備援程度最低】→ 本地備援儲存體（LRS）
三份複本全在同一棟建築物裡，機房一停就全沒了。

【第 2 個】→ 區域備援儲存體（ZRS）
複本跨到同區域的三個可用性區域，撐得過單一資料中心失效，但仍在同一個區域內。

【第 3 個：備援程度最高】→ 異地備援儲存體（GRS）
複本跨到數百公里外的另一個區域，連整個區域的天災都撐得過。三者之中只有它離得開原本的區域。"""

EN162 = """The question wants least redundant to most redundant, and the answer is ⟦LRS → ZRS → GRS⟧. All six storage redundancy options, with copy count and what each survives:
・⟦Locally-redundant storage (LRS)⟧ — three copies in a single physical location inside one datacenter. Survives disk, server and rack failure; does not survive the loss of the datacenter. Eleven nines of annual durability, and the cheapest option.
・⟦Zone-redundant storage (ZRS)⟧ — three copies spread across three availability zones in one region. Survives the loss of a datacenter; does not survive a regional disaster. Twelve nines.
・⟦Geo-redundant storage (GRS)⟧ — LRS in the primary region (three copies) plus asynchronous replication to a paired secondary region hundreds of kilometres away, LRS again (three more), six in all. Survives a regional disaster. Sixteen nines. The secondary is not readable under normal conditions.
・⟦Read-access geo-redundant storage (RA-GRS)⟧ — GRS with the secondary region made readable.
・⟦Geo-zone-redundant storage (GZRS)⟧ — ZRS in the primary region (across three zones) plus LRS in the secondary, covering both datacenter and regional loss. The most complete option.
・⟦Read-access geo-zone-redundant storage (RA-GZRS)⟧ — GZRS with the secondary made readable.
The ordering logic is simply ⟦the wider the blast radius it survives, the more redundant it is⟧: LRS reaches the rack, ZRS the datacenter, GRS the whole region.

[1st — least redundant] -> Locally-redundant storage (LRS)
All three copies sit in one building; lose the building and you lose everything.

[2nd] -> Zone-redundant storage (ZRS)
Copies span three availability zones in the same region, surviving one datacenter but staying inside a single region.

[3rd — most redundant] -> Geo-redundant storage (GRS)
Copies reach a second region hundreds of kilometres away, surviving even a regional disaster. Of the three, only GRS leaves the original region."""

patch(L, 162, """Question #162  ·  Topic 1  ·  DRAG DROP
Arrange the storage account redundancy options from the least redundant to the most redundant. To answer, move all options from the list of options to the answer area and arrange them in the correct order.
Select and Place:

Redundancy options：Zone-redundant storage (ZRS) ｜ Geo-redundant storage (GRS) ｜ Locally-redundant storage (LRS)

Answer Area（紅框標出的正解順序）
1. Locally-redundant storage (LRS)
2. Zone-redundant storage (ZRS)
3. Geo-redundant storage (GRS)

（核對來源：PDF 第 48 頁。答案區是有意義的排序，故 fix:true 不洗答案區）""", line_edits=[
    (" e:", ' e:' + js(E162) + ','),
    ("     e:", '     e:' + js(EN162) + '}},'),
])

# ══ #169（PDF 第 50 頁）══════════════════════════════════════════════
# 原文的描述是名詞片語，反推版本前面多了「是 / is」與「負責」。
E169 = """四個服務分屬完全不同的領域，一次分清楚：
・⟦Azure DevOps⟧— 端對端的開發與交付平台：Boards（工作項目與看板）、Repos（Git 版本控制）、Pipelines（CI/CD 建置與部署）、Test Plans（測試）、Artifacts（套件摘要）。「整合式的程式碼部署解決方案」講的就是它。
・⟦Azure Advisor⟧— 個人化的最佳做法建議引擎，掃描你既有的資源後給出五類建議：可靠性、安全性、效能、成本、卓越營運。它只給建議，不會自己動手改。
・⟦Azure 認知服務（Azure Cognitive Services，現稱 Azure AI 服務）⟧— 一組預先訓練好的 AI API：視覺、語音、語言、決策。不必自己訓練模型也不必懂機器學習，呼叫 REST API 就能加上影像辨識、語音轉文字、翻譯與情感分析。
・⟦Azure Application Insights⟧— Azure 監視器底下的應用程式效能管理（APM）功能，監視執行中的網頁應用程式：要求率與回應時間、失敗率、相依性呼叫、例外狀況、使用者行為，還有即時計量與應用程式對應。
記法：⟦寫程式與部署 → DevOps；只給建議 → Advisor；現成的 AI API → 認知服務；監視應用程式 → Application Insights⟧。

【整合式的程式碼部署解決方案】→ Azure DevOps
關鍵字是「部署程式碼」。Azure DevOps 的 Pipelines 就是做 CI/CD 的地方，從建置到部署一條龍。

【提供指引與建議、協助改善 Azure 環境的工具】→ Azure Advisor
關鍵字是「建議」。四個服務裡只有 Advisor 的產出是建議清單。

【用來建置智慧型人工智慧（AI）應用程式的簡化工具】→ Azure 認知服務（Azure Cognitive Services）
關鍵字是「AI」加「簡化」。要自己訓練模型是 Azure Machine Learning；只想呼叫現成 API 就是認知服務。

【監視網頁應用程式】→ Azure Application Insights
關鍵字是「監視網頁應用程式」。Azure 監視器是整個監視平台，Application Insights 是其中專門看應用程式的那一塊。"""

EN169 = """The four services belong to completely different areas, so separate them once:
・⟦Azure DevOps⟧ — an end-to-end development and delivery platform: Boards (work items and kanban), Repos (Git version control), Pipelines (CI/CD build and release), Test Plans and Artifacts (package feeds). This is what 'an integrated solution for the deployment of code' means.
・⟦Azure Advisor⟧ — a personalised best-practice recommendation engine that scans the resources you already have and reports across five categories: reliability, security, performance, cost and operational excellence. It advises; it never changes anything itself.
・⟦Azure Cognitive Services (now Azure AI services)⟧ — a set of pre-trained AI APIs covering vision, speech, language and decision. No model training and no machine learning knowledge required: call a REST API and you have image recognition, speech-to-text, translation or sentiment analysis.
・⟦Azure Application Insights⟧ — the application performance management (APM) feature inside Azure Monitor, watching a running web application: request rates and response times, failure rates, dependency calls, exceptions, user behaviour, plus live metrics and the application map.
Rule of thumb: ⟦write and ship code → DevOps; recommendations only → Advisor; ready-made AI APIs → Cognitive Services; watch an application → Application Insights⟧.

[An integrated solution for the deployment of code] -> Azure DevOps
The key phrase is 'deployment of code'. Azure DevOps Pipelines is where CI/CD lives, from build through release.

[A tool that provides guidance and recommendations to improve an Azure environment] -> Azure Advisor
The key word is 'recommendations'. Of the four, only Advisor produces a list of recommendations as its output.

[A simplified tool to build intelligent Artificial Intelligence (AI) applications] -> Azure Cognitive Services
The key words are 'AI' and 'simplified'. Training your own model is Azure Machine Learning; calling ready-made APIs is Cognitive Services.

[Monitors web applications] -> Azure Application Insights
The key phrase is 'monitors web applications'. Azure Monitor is the whole monitoring platform; Application Insights is the part of it aimed at applications."""

patch(L, 169, """Question #169  ·  Topic 1  ·  DRAG DROP
Match the Azure service to the correct definition.
Instructions: To answer, drag the appropriate Azure service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Answer Options：Azure Advisor ｜ Azure Cognitive Services ｜ Azure Application Insights ｜ Azure DevOps

Answer Area（紅框標出的正解順序；紅框另外圈出 deployment of code 與 (AI) applications）
1. An integrated solution for the deployment of code　→　Azure DevOps
2. A tool that provides guidance and recommendations to improve an Azure environment　→　Azure Advisor
3. A simplified tool to build intelligent Artificial Intelligence (AI) applications　→　Azure Cognitive Services
4. Monitors web applications　→　Azure Application Insights

（核對來源：PDF 第 50 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦整合式的程式碼部署解決方案⟧",
                             "⟦提供指引與建議、協助改善 Azure 環境的工具⟧",
                             "⟦用來建置智慧型人工智慧（AI）應用程式的簡化工具⟧",
                             "⟦監視網頁應用程式⟧"]) + ','),
    (" e:", ' e:' + js(E169) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦An integrated solution for the deployment of code⟧",
                                     "⟦A tool that provides guidance and recommendations to improve an Azure environment⟧",
                                     "⟦A simplified tool to build intelligent Artificial Intelligence (AI) applications⟧",
                                     "⟦Monitors web applications⟧"]) + ','),
    ("     e:", '     e:' + js(EN169) + '}},'),
])

# ══ #170（PDF 第 50 頁）══════════════════════════════════════════════
E170 = """四個資料服務按「資料長什麼樣、怎麼查」排開：
・⟦Azure SQL Database⟧— 完全受控的關聯式資料庫（PaaS）。以 SQL Server 引擎為底，自動修補、自動備份、內建高可用性；適合交易型（OLTP）工作負載，資料量以 GB 到數 TB 計。
・⟦Azure Synapse Analytics（原 SQL 資料倉儲）⟧— 分析型（OLAP）的資料倉儲。核心是⟦大規模平行處理（MPP）⟧：把一張大表切成多個分散區，由多個運算節點同時掃描再彙總，所以能在數 PB 的關聯式資料上跑複雜查詢。
・⟦Azure Data Lake Analytics⟧— 隨選的分散式分析作業服務，用 U-SQL 撰寫大規模平行的資料轉換與處理程式，直接對 Data Lake Store 裡的檔案執行，依作業實際用掉的分析單位計費。它處理的是「檔案」，不是「資料表」。
・⟦Azure HDInsight⟧— 受控的開放原始碼叢集服務，把 Hadoop、Spark、Hive、Kafka、HBase 這些⟦開放原始碼架構⟧開好給你，用叢集做分散式處理與分析。
分辨訣竅：⟦「關聯式 + 受控」→ SQL Database；「MPP + 關聯式 + PB 級查詢」→ Synapse；「平行的轉換與處理程式 + 檔案」→ Data Lake Analytics；「開放原始碼架構 + 叢集」→ HDInsight⟧。
提醒：Azure Data Lake Analytics 目前已較少被推薦，Microsoft 建議新專案改用 Azure Synapse Analytics 的 Spark 集區或 Azure Databricks，但考題仍會考它的定位。

【受控的關聯式雲端資料庫服務】→ Azure SQL Database
四個裡面只有它是「資料庫」而不是「分析平台」，而且明講關聯式。

【運用大規模平行處理（MPP），在關聯式資料庫中對數 PB 的資料快速執行複雜查詢的雲端服務】→ Azure SQL Synapse Analytics
關鍵字是 MPP 加「關聯式資料庫」。同樣是 PB 級，但資料仍在關聯式資料表裡，所以不是 Data Lake Analytics。

【可以在數 PB 的資料上執行大規模平行的資料轉換與處理程式】→ Azure Data Lake Analytics
關鍵字是「轉換與處理程式」——你寫的是作業（U-SQL 程式），不是查詢資料表。

【提供在叢集中分散式處理與分析巨量資料集的開放原始碼架構】→ Azure HDInsight
關鍵字是「開放原始碼」加「叢集」。題目直接點名開放原始碼架構，那就是 HDInsight。"""

EN170 = """Line the four data services up by what the data looks like and how it is queried:
・⟦Azure SQL Database⟧ — a fully managed relational database (PaaS). Built on the SQL Server engine with automatic patching, automatic backup and built-in high availability; suited to transactional (OLTP) workloads sized in GB to a few TB.
・⟦Azure Synapse Analytics (formerly SQL Data Warehouse)⟧ — the analytical (OLAP) data warehouse. Its core is ⟦massively parallel processing (MPP)⟧: a large table is split into distributions and scanned by many compute nodes at once, then aggregated, which is how it runs complex queries across petabytes of relational data.
・⟦Azure Data Lake Analytics⟧ — an on-demand distributed analytics job service. You write massively parallel data transformation and processing programs in U-SQL that run directly over files in Data Lake Store, billed by the analytics units a job actually consumes. It processes files, not tables.
・⟦Azure HDInsight⟧ — managed open-source cluster service, standing up Hadoop, Spark, Hive, Kafka and HBase — ⟦open-source frameworks⟧ — for distributed processing and analysis on clusters.
Rule of thumb: ⟦'relational + managed' → SQL Database; 'MPP + relational + petabyte queries' → Synapse; 'parallel transformation and processing programs + files' → Data Lake Analytics; 'open-source framework + clusters' → HDInsight⟧.
Note: Azure Data Lake Analytics is rarely recommended now — Microsoft steers new projects to Azure Synapse Analytics Spark pools or Azure Databricks — but exams still test where it sits.

[A managed relational cloud database service] -> Azure SQL Database
It is the only one of the four that is a database rather than an analytics platform, and it says relational outright.

[A cloud-based service that leverages massively parallel processing (MPP) to quickly run complex queries across petabytes of data in a relational database] -> Azure SQL Synapse Analytics
The key words are MPP and 'relational database'. Petabyte scale again, but the data still sits in relational tables, so this is not Data Lake Analytics.

[Can run massively parallel data transformation and processing programs across petabytes of data] -> Azure Data Lake Analytics
The key phrase is 'transformation and processing programs' — you write jobs (U-SQL programs), not table queries.

[An open-source framework for the distributed processing and analysis of big data sets in clusters] -> Azure HDInsight
The key words are 'open-source' and 'clusters'. The question names the open-source framework outright, which is HDInsight."""

patch(L, 170, """Question #170  ·  Topic 1  ·  DRAG DROP
Match the Azure service to the correct description.
Instructions: To answer, drag the appropriate Azure service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Answer Options：Azure HDInsight ｜ Azure Data Lake Analytics ｜ Azure SQL Synapse Analytics ｜ Azure SQL Database

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. A [managed relational cloud database] service.　→　Azure SQL Database
2. A cloud-based service that leverages [massively parallel processing (MPP)] to quickly run complex queries across petabytes of data in a relational database.　→　Azure SQL Synapse Analytics
3. Can run massively parallel data [transformation and processing programs] across petabytes of data　→　Azure Data Lake Analytics
4. An [open-source] framework for the distributed processing and analysis of big data sets in clusters　→　Azure HDInsight

（核對來源：PDF 第 50 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦受控的關聯式雲端資料庫服務⟧",
                             "運用⟦大規模平行處理（MPP）⟧，在關聯式資料庫中對數 PB 的資料快速執行複雜查詢的雲端服務",
                             "可以在數 PB 的資料上執行大規模平行的⟦資料轉換與處理程式⟧",
                             "提供在叢集中分散式處理與分析巨量資料集的⟦開放原始碼⟧架構"]) + ','),
    (" e:", ' e:' + js(E170) + ','),
    ("     tgt:[", '     tgt:' + arr(["A ⟦managed relational cloud database⟧ service",
                                     "A cloud-based service that leverages ⟦massively parallel processing (MPP)⟧ to quickly run complex queries across petabytes of data in a relational database",
                                     "Can run massively parallel data ⟦transformation and processing programs⟧ across petabytes of data",
                                     "An ⟦open-source⟧ framework for the distributed processing and analysis of big data sets in clusters"]) + ','),
    ("     e:", '     e:' + js(EN170) + '}},'),
])

# ══ #171（PDF 第 51 頁）══════════════════════════════════════════════
# 原文三個下拉的選項順序都是 Monitor / Subscriptions / Marketplace / Advisor，
# 反推版本把正解排到各格第一個；改回原文順序並重對 a。
BLADES = ["監視器（Monitor）", "訂用帳戶（Subscriptions）", "市集（Marketplace）", "建議程式（Advisor）"]
BLADES_EN = ["Monitor", "Subscriptions", "Marketplace", "Advisor"]

E171 = """Azure 入口網站幾個刀鋒視窗的分工：
・⟦監視器（Monitor）⟧— 收集與檢視計量、記錄與警示的總入口；底下含 Application Insights（應用程式）、Log Analytics（記錄查詢）與服務健康狀態（Azure 服務本身的中斷、計畫維護與健康狀況建議）。要看「Azure 服務健不健康」就從這裡進去。
・⟦市集（Marketplace）⟧— 第一方與第三方的虛擬機器映像、虛擬設備、SaaS 應用程式與解決方案範本的目錄。虛擬機器映像就在這裡瀏覽與部署。
・⟦建議程式（Advisor）⟧— 個人化建議：可靠性、安全性、效能、成本、卓越營運五類。其中的安全性建議來自 Microsoft Defender for Cloud，在 Advisor 一起呈現。
・⟦訂用帳戶（Subscriptions）⟧— 訂用帳戶清單、計費、資源計數與存取控制。與上面三件工作都無關，是本題的干擾項。
提醒：入口網站左側的「建立資源」按鈕其實就是 Marketplace 的入口，兩者是同一個地方。

【監視 Azure 服務的健康狀態】→ 監視器（Monitor）
注意是「Azure 服務」的健康狀態，不是你自己應用程式的健康狀態；前者在監視器底下的服務健康狀態，後者才是 Application Insights。

【瀏覽可用的虛擬機器映像】→ 市集（Marketplace）
「瀏覽映像」＝逛目錄，那就是市集。

【檢視安全性建議】→ 建議程式（Advisor）
「建議」兩個字直接指向 Advisor。安全性建議是它五類建議中的一類。"""

EN171 = """How the Azure portal blades divide the work:
・⟦Monitor⟧ — the front door for metrics, logs and alerts, with Application Insights (applications), Log Analytics (log queries) and Service Health (outages, planned maintenance and health advisories for Azure itself) underneath it. 'Is the Azure service healthy' starts here.
・⟦Marketplace⟧ — the catalogue of first- and third-party virtual machine images, virtual appliances, SaaS applications and solution templates. Browsing and deploying VM images happens here.
・⟦Advisor⟧ — personalised recommendations across five categories: reliability, security, performance, cost and operational excellence. The security recommendations come from Microsoft Defender for Cloud and are surfaced here alongside the rest.
・⟦Subscriptions⟧ — the subscription list, billing, resource counts and access control. Unrelated to all three tasks and the distractor in this question.
Note: the 'Create a resource' button on the left of the portal is the Marketplace — the same place under another name.

[Monitor the health of Azure services] -> Monitor
Note that this is the health of the Azure services, not of your own application: the former is Service Health under Monitor, the latter is Application Insights.

[Browse available virtual machine images] -> Marketplace
'Browse images' means browsing a catalogue, and the catalogue is the Marketplace.

[View security recommendations] -> Advisor
The word 'recommendations' points straight at Advisor; security is one of its five categories."""

patch(L, 171, """Question #171  ·  Topic 1  ·  HOTSPOT
You need to identify which blades in the Azure portal must be used to perform the following tasks:
➯ View security recommendations.
➯ Monitor the health of Azure services.
➯ Browse available virtual machine images.
Which blade should you identify for each task? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.

Answer Area（三個下拉的選項都是 Monitor ｜ Subscriptions ｜ Marketplace ｜ Advisor）
1. Monitor the health of Azure services:　→　Monitor
2. Browse available virtual machine images:　→　Marketplace
3. View security recommendations:　→　Advisor

（核對來源：PDF 第 51 頁）""", line_edits=[
    (" q:", ' q:' + js("你要找出在 Azure 入口網站中，執行下列工作各該使用哪一個刀鋒視窗（blade）：\n"
                       "・檢視安全性建議。\n・監視 Azure 服務的健康狀態。\n・瀏覽可用的虛擬機器映像。\n"
                       "每一項工作各該選哪一個刀鋒視窗？請在答案區選出正確的選項。") + ','),
    (" dd:[", ' dd:' + arr2([BLADES, BLADES, BLADES]) + ','),
    (" a:[", ' a:[0,2,3],'),
    (" e:", ' e:' + js(E171) + ','),
    (" en:{q:", ' en:{q:' + js("You need to identify which blades in the Azure portal must be used to perform the following tasks:\n"
                               "・View security recommendations.\n・Monitor the health of Azure services.\n・Browse available virtual machine images.\n"
                               "Which blade should you identify for each task? To answer, select the appropriate options in the answer area.") + ','),
    ("     dd:[", '     dd:' + arr2([BLADES_EN, BLADES_EN, BLADES_EN]) + ','),
    ("     e:", '     e:' + js(EN171) + '}},'),
])

save(L)
print("批次 C 完成：#149 #150 #161 #162 #169 #170 #171")
