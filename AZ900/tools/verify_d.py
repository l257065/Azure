# -*- coding: utf-8 -*-
"""核對原文 批次 D：#180 #187 #202 #224 #243（PDF 第 53、56、60、66、72 頁）。
   同時把解析改寫成「共用對照一次 + 逐格重點」。一次性腳本，保留供追溯。"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, js, arr, arr2

L = load()

# ══ #180（PDF 第 53 頁）══════════════════════════════════════════════
E180 = """四個服務分屬完全不同的領域，一次分清楚：
・⟦Azure Synapse Analytics⟧— 企業級的資料倉儲與分析平台（前身是 SQL 資料倉儲）。用大規模平行處理（MPP）在 PB 級的結構化資料上跑分析查詢，並整合 Spark 集區、資料整合管線與 Power BI。「企業資料倉儲（EDW）」講的就是它。
・⟦Azure Machine Learning⟧— 端對端的機器學習平台：準備資料、訓練模型、評估、註冊、部署成端點、監視漂移。核心動作是「用過去的資料訓練出模型，再拿模型預測未來」。
・⟦Azure Functions⟧— 事件驅動的無伺服器運算。寫一段函式、設好觸發程序（HTTP、計時器、佇列、Blob…），平台在事件發生時執行，依執行次數與執行時間計費，不執行不收費。
・⟦Azure IoT 中樞（Azure IoT Hub）⟧— 裝置與雲端之間的雙向訊息中樞，可同時連上數百萬台裝置，接收遙測也能回送命令與更新設定。
記法：⟦資料倉儲 → Synapse；訓練與預測 → Machine Learning；無伺服器 → Functions；感應器與裝置 → IoT 中樞⟧。

【提供雲端的企業資料倉儲（EDW）】→ Azure Synapse Analytics
關鍵字是「資料倉儲」。EDW 存的是整理過、可直接分析的結構化資料。

【運用過去的訓練，提供高機率的預測結果】→ Azure Machine Learning
關鍵字是「訓練」與「預測」。凡是先訓練模型再拿去推論的，就是 Machine Learning；只想呼叫現成 AI API 則是認知服務。

【提供無伺服器運算功能】→ Azure Functions
關鍵字是「無伺服器」。Azure 上典型的無伺服器組合是 Functions（運算）＋ Logic Apps（流程）＋ Event Grid（事件）。

【處理來自數百萬個感應器的資料】→ Azure IoT 中樞（Azure IoT Hub）
關鍵字是「數百萬個感應器」。裝置規模一大就是 IoT 中樞；純粹的高流量事件擷取則會考慮 Event Hubs。"""

EN180 = """The four services sit in completely different areas, so separate them once:
・⟦Azure Synapse Analytics⟧ — the enterprise data warehouse and analytics platform (formerly SQL Data Warehouse). Massively parallel processing (MPP) runs analytical queries over petabytes of structured data, with Spark pools, data integration pipelines and Power BI integrated. 'Enterprise Data Warehouse (EDW)' means this.
・⟦Azure Machine Learning⟧ — the end-to-end ML platform: prepare data, train models, evaluate, register, deploy as endpoints, monitor for drift. The core motion is training a model on past data and then predicting with it.
・⟦Azure Functions⟧ — event-driven serverless compute. Write a function, configure a trigger (HTTP, timer, queue, blob), and the platform runs it when the event fires, billed by execution count and duration, with nothing to pay when idle.
・⟦Azure IoT Hub⟧ — the bidirectional message hub between devices and the cloud, able to connect millions of devices at once, taking telemetry up and sending commands and configuration back down.
Rule of thumb: ⟦data warehouse → Synapse; training and prediction → Machine Learning; serverless → Functions; sensors and devices → IoT Hub⟧.

[Provides a cloud-based Enterprise Data Warehouse (EDW)] -> Azure Synapse Analytics
The key phrase is data warehouse: an EDW holds curated, analysis-ready structured data.

[Uses past trainings to provide predictions that have high probability] -> Azure Machine Learning
The key words are training and prediction. Train a model then infer with it and you are in Machine Learning; call a ready-made AI API and you are in Cognitive Services.

[Provides serverless computing functionalities] -> Azure Functions
The key word is serverless. The classic Azure serverless trio is Functions (compute), Logic Apps (workflow) and Event Grid (events).

[Processes data from millions of sensors] -> Azure IoT Hub
The key phrase is 'millions of sensors'. Device scale points to IoT Hub; pure high-throughput event ingestion would point to Event Hubs."""

patch(L, 180, """Question #180  ·  Topic 1  ·  DRAG DROP
Match the Azure services to the correct descriptions.
Instructions: To answer, drag the appropriate Azure service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point
Select and Place:

Azure Services：Azure Machine Learning ｜ Azure Synapse Analytics ｜ Azure IoT Hub ｜ Azure Functions

Answer Area（紅框標出的正解順序；描述裡的 [ ] 是紅框另外圈起來的關鍵字）
1. Provides a cloud-based Enterprise [Data Warehouse (EDW).]　→　Azure Synapse Analytics
2. Uses past [trainings] to provide predictions that have high probability.　→　Azure Machine Learning
3. Provides serverless computing [functionalities.]　→　Azure Functions
4. Processes data from [millions of sensors.]　→　Azure IoT Hub

（核對來源：PDF 第 53 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["提供雲端的⟦企業資料倉儲（EDW）⟧",
                             "運用過去的⟦訓練⟧，提供高機率的預測結果",
                             "提供無伺服器⟦運算功能⟧",
                             "處理來自⟦數百萬個感應器⟧的資料"]) + ','),
    (" e:", ' e:' + js(E180) + ','),
    ("     tgt:[", '     tgt:' + arr(["Provides a cloud-based Enterprise ⟦Data Warehouse (EDW)⟧",
                                     "Uses past ⟦trainings⟧ to provide predictions that have high probability",
                                     "Provides serverless computing ⟦functionalities⟧",
                                     "Processes data from ⟦millions of sensors⟧"]) + ','),
    ("     e:", '     e:' + js(EN180) + '}},'),
])

# ══ #187（PDF 第 56 頁）══════════════════════════════════════════════
# 原文三個下拉的選項順序相同，正解都排在第四個；反推版本把正解搬到第一個。
TOOLS = ["只有 Azure CLI 與 Azure 入口網站",
         "只有 Azure 入口網站與 Azure PowerShell",
         "只有 Azure CLI 與 Azure PowerShell",
         "Azure CLI、Azure 入口網站與 Azure PowerShell 三者都可以"]
TOOLS_EN = ["The Azure CLI and the Azure portal",
            "The Azure portal and Azure PowerShell",
            "The Azure CLI and Azure PowerShell",
            "The Azure CLI, the Azure portal, and Azure PowerShell"]

E187 = """三個管理工具的跨平台支援，一次列清楚：
・⟦Azure 入口網站（Azure portal）⟧— 網頁介面，任何有現代瀏覽器的裝置都能用：Windows、Linux、macOS、平板、手機都可以，完全與作業系統無關。
・⟦Azure CLI⟧— 跨平台的命令列工具，Windows、Linux、macOS 都有原生安裝套件。語法是 `az 群組 子命令`，輸出可轉成 JSON、表格或 TSV。
・⟦Azure PowerShell⟧— 現在的 Az 模組建構在 ⟦PowerShell 7（原 PowerShell Core）⟧ 上，Windows、Linux、macOS 都能安裝。語法是 `動詞-Az名詞`，例如 New-AzVM。
所以三台電腦的答案完全一樣：⟦三個工具全都可以用⟧。這一題的陷阱是把 Azure PowerShell 誤認成只有 Windows 能跑的舊 Windows PowerShell —— 自 PowerShell Core 起早就跨平台了。
補一個常考點：⟦Azure Cloud Shell⟧ 連裝都不用裝，瀏覽器裡就有 Bash 與 PowerShell 兩種殼層，並自動掛載一個儲存體帳戶保存檔案；只要開得了瀏覽器，任何作業系統都能用 CLI 與 PowerShell。

【Computer1（Windows 10）】→ 三者都可以
Windows 上三個工具本來就都能裝，沒有懸念。

【Computer2（Ubuntu）】→ 三者都可以
Linux 上 CLI 與 PowerShell（Az 模組跑在 PowerShell 7）都有官方安裝套件，入口網站用瀏覽器開。

【Computer3（MacOS Mojave）】→ 三者都可以
macOS 同樣可以用 Homebrew 裝 Azure CLI 與 PowerShell 7，入口網站一樣用瀏覽器。"""

EN187 = """Cross-platform support for the three management tools, laid out once:
・⟦The Azure portal⟧ — a web interface usable from any device with a modern browser: Windows, Linux, macOS, tablet or phone. Entirely independent of the operating system.
・⟦The Azure CLI⟧ — a cross-platform command-line tool with native packages for Windows, Linux and macOS. The syntax is `az <group> <command>`, with output as JSON, table or TSV.
・⟦Azure PowerShell⟧ — today's Az module is built on ⟦PowerShell 7 (formerly PowerShell Core)⟧ and installs on Windows, Linux and macOS alike. The syntax is `Verb-AzNoun`, for example New-AzVM.
So all three computers get the same answer: ⟦all three tools work⟧. The trap is mistaking Azure PowerShell for the old Windows-only Windows PowerShell; it has been cross-platform since PowerShell Core.
Worth adding, because it is often tested: ⟦Azure Cloud Shell⟧ requires no installation at all — Bash and PowerShell shells in the browser, with a storage account mounted automatically for your files. Any OS that can open a browser can use the CLI and PowerShell.

[Computer1 (Windows 10)] -> all three
All three install on Windows; nothing controversial here.

[Computer2 (Ubuntu)] -> all three
Linux has official packages for the CLI and for PowerShell 7 (which hosts the Az module), and the portal opens in a browser.

[Computer3 (MacOS Mojave)] -> all three
macOS installs the Azure CLI and PowerShell 7 via Homebrew, and the portal again opens in a browser."""

patch(L, 187, """Question #187  ·  Topic 1  ·  HOTSPOT
Several support engineers plan to manage Azure by using the computers shown in the following table:

Name       ｜ Operating system
Computer1  ｜ Windows 10
Computer2  ｜ Ubuntu
Computer3  ｜ MacOS Mojave

You need to identify which Azure management tools can be used from each computer.
What should you identify for each computer? To answer, select the appropriate options in the answer area.

Answer Area（三個下拉的選項都是同一組，順序如下）
The Azure CLI and the Azure portal ｜ The Azure portal and Azure PowerShell ｜ The Azure CLI and Azure PowerShell ｜ The Azure CLI, the Azure portal, and Azure PowerShell

紅框標出的正解
1. Computer1　→　The Azure CLI, the Azure portal, and Azure PowerShell
2. Computer2　→　The Azure CLI, the Azure portal, and Azure PowerShell
3. Computer3　→　The Azure CLI, the Azure portal, and Azure PowerShell

（核對來源：PDF 第 56 頁）""", line_edits=[
    (" q:", ' q:' + js("有數名支援工程師打算用下列電腦來管理 Azure。\n"
                       "你要找出每一台電腦各能使用哪些 Azure 管理工具。每一台電腦各該選什麼？請在答案區選出正確的選項。") + ','),
    (" dd:[", ' dd:' + arr2([TOOLS, TOOLS, TOOLS]) + ','),
    (" a:[", ' a:[3,3,3],'),
    (" e:", ' e:' + js(E187) + ','),
    (" en:{q:", ' en:{q:' + js("Several support engineers plan to manage Azure by using the computers shown in the following table.\n"
                               "You need to identify which Azure management tools can be used from each computer.\n"
                               "What should you identify for each computer? To answer, select the appropriate options in the answer area.") + ','),
    ("     dd:[", '     dd:' + arr2([TOOLS_EN, TOOLS_EN, TOOLS_EN]) + ','),
    ("     e:", '     e:' + js(EN187) + '}},'),
])

# ══ #202（PDF 第 60 頁）══════════════════════════════════════════════
E202 = """四個服務一次分清楚：
・⟦Azure Functions⟧— 事件驅動的無伺服器運算平台。寫一段函式、設好觸發程序，平台在事件發生時執行，依執行次數與執行時間計費，閒置不收費。適合短工作、排程作業、事件處理。
・⟦Azure Databricks⟧— 以 Apache Spark 為基礎的分析平台：協作式筆記本、受控的 Spark 叢集、Delta Lake 與 MLflow。資料工程與機器學習的大規模資料處理都在這裡做。
・⟦Azure Application Insights⟧— Azure 監視器底下的應用程式效能管理（APM）：要求率與回應時間、失敗率、相依性呼叫、例外狀況、使用者行為；內建的智慧偵測會自動找出效能與失敗的異常並發出警示。
・⟦Azure App Service⟧— 裝載網頁應用程式、REST API 與行動後端的平台即服務（PaaS）；平台負責作業系統修補、執行階段更新、負載平衡與自動調整規模。
兩組容易混淆的要一起記：⟦Functions（無伺服器、事件觸發、短工作）對 App Service（長時間執行的網站與 API）⟧；⟦Databricks（Spark 大數據與機器學習）對 Synapse（關聯式資料倉儲與 MPP 查詢）⟧。

【提供無伺服器程式碼的執行平台】→ Azure Functions
關鍵字是「無伺服器」。同樣能跑程式碼的 App Service 是常駐的主控環境，不是無伺服器。

【供機器學習使用的巨量資料分析服務】→ Azure Databricks
關鍵字是「巨量資料」加「機器學習」。兩個字同時出現，指的是 Spark 這一系，也就是 Databricks。

【偵測並診斷網頁應用程式的異常】→ Azure Application Insights
關鍵字是「異常」。Application Insights 的智慧偵測就是專門做這件事的。

【裝載網頁應用程式】→ Azure App Service
關鍵字是「裝載」。這是 App Service 最本份的工作。"""

EN202 = """Separate the four services once:
・⟦Azure Functions⟧ — an event-driven serverless compute platform. Write a function, configure a trigger, and the platform runs it when the event fires, billed by execution count and duration with nothing to pay while idle. Good for short jobs, scheduled work and event handling.
・⟦Azure Databricks⟧ — an Apache Spark-based analytics platform: collaborative notebooks, managed Spark clusters, Delta Lake and MLflow. Large-scale data engineering and machine learning happen here.
・⟦Azure Application Insights⟧ — the application performance management (APM) feature inside Azure Monitor: request rates and response times, failure rates, dependency calls, exceptions and user behaviour, with built-in Smart Detection that surfaces performance and failure anomalies and raises alerts.
・⟦Azure App Service⟧ — platform as a service (PaaS) hosting for web apps, REST APIs and mobile back ends, where the platform owns OS patching, runtime updates, load balancing and autoscale.
Two pairs worth learning together: ⟦Functions (serverless, event-triggered, short jobs) against App Service (long-running sites and APIs)⟧, and ⟦Databricks (Spark big data and ML) against Synapse (relational warehousing and MPP queries)⟧.

[Provides the platform for serverless code] -> Azure Functions
The key word is serverless. App Service also runs your code, but as always-on hosting rather than serverless.

[A big data analysis service for machine learning] -> Azure Databricks
The key phrases are big data and machine learning. Together they point at the Spark family, which is Databricks.

[Detects and diagnoses anomalies in web apps] -> Azure Application Insights
The key word is anomalies, and Smart Detection in Application Insights exists for exactly this.

[Hosts web apps] -> Azure App Service
The key word is hosts, which is App Service's core job."""

patch(L, 202, """Question #202  ·  Topic 1  ·  DRAG DROP
Match the Azure service to the correct definition.
Instructions: To answer, drag the appropriate Azure service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct selection is worth one point.
Select and Place:

Answer Options：Azure Databricks ｜ Azure Functions ｜ Azure App Service ｜ Azure Application Insights

Answer Area（紅框標出的正解順序）
1. Provides the platform for serverless code　→　Azure Functions
2. A big data analysis service for machine learning　→　Azure Databricks
3. Detects and diagnoses anomalies in web apps　→　Azure Application Insights
4. Hosts web apps　→　Azure App Service

（核對來源：PDF 第 60 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["提供⟦無伺服器程式碼的執行平台⟧",
                             "⟦供機器學習使用的巨量資料分析服務⟧",
                             "⟦偵測並診斷網頁應用程式的異常⟧",
                             "⟦裝載網頁應用程式⟧"]) + ','),
    (" e:", ' e:' + js(E202) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Provides the platform for serverless code⟧",
                                     "⟦A big data analysis service for machine learning⟧",
                                     "⟦Detects and diagnoses anomalies in web apps⟧",
                                     "⟦Hosts web apps⟧"]) + ','),
    ("     e:", '     e:' + js(EN202) + '}},'),
])

# ══ #224（PDF 第 66 頁）══════════════════════════════════════════════
# 原文可拖曳欄有五個服務（含 Azure AD 與 Azure Lighthouse 兩個干擾項），
# 反推版本只留下三個用得到的；把兩個干擾項補回來並重對 a。
SEC = ["Azure Active Directory（Azure AD）", "Azure Key Vault", "Azure Lighthouse", "Azure 資訊安全中心（Azure Security Center）", "Azure Sentinel"]
SEC_EN = ["Azure Active Directory (Azure AD)", "Azure Key Vault", "Azure Lighthouse", "Azure Security Center", "Azure Sentinel"]

E224 = """原文的可拖曳欄有五個服務，答案區只有三格，⟦Azure Active Directory 與 Azure Lighthouse 是沒有用到的干擾項⟧。五個一起記：
・⟦Azure Sentinel（現稱 Microsoft Sentinel）⟧— 雲端原生的 SIEM 與 SOAR。用資料連接器把 Azure、地端與其他雲的記錄檔集中到 Log Analytics 工作區，做關聯分析與威脅偵測，再用劇本（playbook，底層是 Logic Apps）自動回應事件。
・⟦Azure 資訊安全中心（Azure Security Center，現稱 Microsoft Defender for Cloud）⟧— 雲端安全狀態管理（CSPM）加工作負載保護（CWPP）。它算出並顯示⟦安全分數（secure score）⟧，也提供法規遵循儀表板與逐項強化建議。
・⟦Azure Key Vault⟧— 集中保管密碼、連線字串、API 金鑰、憑證與加密金鑰，支援硬體安全模組（HSM）保護、存取原則或 RBAC 授權、版本管理與自動輪替。應用程式用受控識別去取，程式碼裡就不必留任何密碼。
・⟦Azure Active Directory（現稱 Microsoft Entra ID）⟧— 雲端的身分與存取管理：使用者、群組、單一登入、多重要素驗證、條件式存取。它管「誰是誰」，不是拿來保管密碼的地方。
・⟦Azure Lighthouse⟧— 委派資源管理，讓服務提供者從自己的租用戶跨租用戶去管理客戶的訂用帳戶與資源群組。
一句話分：⟦Sentinel 看記錄找威脅、資訊安全中心給分數與強化建議、Key Vault 存祕密、Azure AD 管身分、Lighthouse 跨租用戶代管⟧。

【分析來自 Azure 虛擬機器的安全性記錄檔案】→ Azure Sentinel
關鍵字是「記錄檔案」加「分析」。集中收記錄再做關聯分析是 SIEM 的本業。

【顯示某個 Azure 訂用帳戶的安全分數（secure score）】→ Azure Security Center
關鍵字是「安全分數」。這個分數是資訊安全中心（Defender for Cloud）獨有的指標。

【儲存供 Azure Function 應用程式使用的密碼】→ Azure Key Vault
關鍵字是「儲存密碼」。這題最容易誤選 Azure AD——Azure AD 管的是身分，保管密碼與金鑰的是 Key Vault。"""

EN224 = """The source lists five services but the answer area has only three boxes — ⟦Azure Active Directory and Azure Lighthouse are the unused distractors⟧. Learn all five together:
・⟦Azure Sentinel (now Microsoft Sentinel)⟧ — cloud-native SIEM and SOAR. Data connectors pull logs from Azure, on-premises and other clouds into a Log Analytics workspace for correlation and threat detection, and playbooks (Logic Apps underneath) respond to incidents automatically.
・⟦Azure Security Center (now Microsoft Defender for Cloud)⟧ — cloud security posture management (CSPM) plus workload protection (CWPP). It calculates and displays the ⟦secure score⟧, and offers a regulatory compliance dashboard with itemised hardening recommendations.
・⟦Azure Key Vault⟧ — central custody of passwords, connection strings, API keys, certificates and encryption keys, with hardware security module (HSM) protection, access policies or RBAC, versioning and automatic rotation. Applications fetch them with a managed identity, so no secret ever sits in code.
・⟦Azure Active Directory (now Microsoft Entra ID)⟧ — cloud identity and access management: users, groups, single sign-on, multi-factor authentication, conditional access. It governs who someone is; it is not a vault for secrets.
・⟦Azure Lighthouse⟧ — delegated resource management, letting a service provider manage a customer's subscriptions and resource groups across tenants from its own tenant.
One line apiece: ⟦Sentinel hunts threats in logs, Security Center scores and hardens, Key Vault stores secrets, Azure AD manages identity, Lighthouse manages across tenants⟧.

[Analyze security log files from Azure virtual machines] -> Azure Sentinel
The key words are log files and analyze. Centralising logs and correlating them is exactly what a SIEM does.

[Display the secure score for an Azure subscription] -> Azure Security Center
The key phrase is secure score, a metric unique to Security Center (Defender for Cloud).

[Store passwords for use by Azure Function applications] -> Azure Key Vault
The key phrase is storing passwords. The tempting wrong answer here is Azure AD — Azure AD manages identities, while Key Vault is what holds secrets and keys."""

patch(L, 224, """Question #224  ·  Topic 1  ·  DRAG DROP
Match the Azure Services service to the correct descriptions.
Instructions: To answer, drag the appropriate service from the column on the left to its description on the right. Each service may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Services：Azure Active Directory (Azure AD) ｜ Azure Key Vault ｜ Azure Lighthouse ｜ Azure Security Center ｜ Azure Sentinel

Answer Area（紅框標出的正解順序）
1. Analyze security log files from Azure virtual machines　→　Azure Sentinel
2. Display the secure score for an Azure subscription　→　Azure Security Center
3. Store passwords for use by Azure Function applications.　→　Azure Key Vault

（核對來源：PDF 第 66 頁。原文有五個可拖曳項目，Azure AD 與 Azure Lighthouse 沒有用到）""", line_edits=[
    (" items:[", ' items:' + arr(SEC) + ','),
    (" tgt:[", ' tgt:' + arr(["⟦分析來自 Azure 虛擬機器的安全性記錄檔案⟧",
                             "⟦顯示某個 Azure 訂用帳戶的安全分數（secure score）⟧",
                             "⟦儲存供 Azure Function 應用程式使用的密碼⟧"]) + ','),
    (" a:[", ' a:[4,3,1],'),
    (" e:", ' e:' + js(E224) + ','),
    ("     items:[", '     items:' + arr(SEC_EN) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Analyze security log files from Azure virtual machines⟧",
                                     "⟦Display the secure score for an Azure subscription⟧",
                                     "⟦Store passwords for use by Azure Function applications⟧"]) + ','),
    ("     e:", '     e:' + js(EN224) + '}},'),
])

# ══ #243（PDF 第 72 頁）══════════════════════════════════════════════
# 原文的描述是名詞片語，反推版本前面多了「指的是…的能力／這個流程／的機制」。
E243 = """身分識別的幾個詞常被混在一起，一次分清楚：
・⟦驗證（authentication）⟧— 回答「你是誰」。用密碼、憑證、生物特徵等方式證明身分。
・⟦授權（authorization）⟧— 回答「你可以做什麼」。身分確認之後，判斷這個使用者或服務對哪些資源有什麼層級的存取權；Azure 用 RBAC 角色指派來做。
・⟦多重要素驗證（MFA）⟧— 驗證的加強版，要求⟦兩種以上不同類別的要素⟧：你知道的（密碼、PIN）、你擁有的（手機、硬體權杖、驗證器 App）、你本身的（指紋、臉部）。同一類別的兩個東西不算，兩組密碼不是 MFA。
・⟦單一登入（SSO）⟧— 登入一次之後，同一組憑證就能存取多個資源與應用程式，包括不同提供者的服務。密碼變少，被竊的機會也跟著變少。
順序記法：⟦先 authentication（可用 MFA 強化）→ 再 authorization；SSO 是讓 authentication 只需要做一次⟧。

【能用同一組憑證，存取來自不同提供者的多個資源與應用程式的能力】→ 單一登入（SSO）
關鍵字是「同一組憑證」加「多個資源」。跨提供者這一點正是 SSO 靠同盟（federation）做到的。

【判斷使用者或服務存取層級的流程】→ 授權（authorization）
關鍵字是「存取層級」。談到「能做什麼、有多少權限」就是授權，不是驗證。

【需要多項要素才能確認使用者或服務身分】→ 多重要素驗證（MFA）
關鍵字是「多項要素」。注意要素必須分屬不同類別才算數。"""

EN243 = """The identity vocabulary blurs together easily, so separate it once:
・⟦Authentication⟧ — answers 'who are you', proving identity with a password, certificate or biometric.
・⟦Authorization⟧ — answers 'what may you do'. Once identity is established, it decides what level of access this user or service has to which resources; Azure does it with RBAC role assignments.
・⟦Multi-factor authentication (MFA)⟧ — authentication reinforced, requiring ⟦two or more factors from different categories⟧: something you know (password, PIN), something you have (phone, hardware token, authenticator app), something you are (fingerprint, face). Two things from the same category do not count — two passwords is not MFA.
・⟦Single sign-on (SSO)⟧ — sign in once and the same credentials reach multiple resources and applications, including services from different providers. Fewer passwords means fewer passwords to steal.
Order to remember: ⟦authentication first (optionally strengthened with MFA), then authorization; SSO is what makes authentication happen only once⟧.

[The ability to use the same credentials to access multiple resources and applications from different providers] -> single sign-on (SSO)
The key phrases are 'same credentials' and 'multiple resources'. Reaching across providers is precisely what SSO achieves through federation.

[The process of identifying the access level of a user or service] -> authorization
The key phrase is 'access level'. Anything about what may be done, and how much permission there is, is authorization rather than authentication.

[Requires several elements to identify a user or service] -> multi-factor authentication (MFA)
The key phrase is 'several elements'. Note that the elements must come from different categories to count."""

patch(L, 243, """Question #243  ·  Topic 1  ·  DRAG DROP
Match the term to the appropriate description.
To answer, drag the appropriate term from the column on the left to its description on the right. Each term may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Terms：authorization ｜ multi-factor authentication (MFA) ｜ single sign-on (SSO)

Answer Area（紅框標出的正解順序）
1. The ability to use the same credentials to access multiple resources and applications from different providers.　→　single sign-on (SSO)
2. The process of identifying the access level of a user or service.　→　authorization
3. Requires several elements to identify a user or service.　→　multi-factor authentication (MFA)

（核對來源：PDF 第 72 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦能用同一組憑證，存取來自不同提供者的多個資源與應用程式的能力⟧",
                             "⟦判斷使用者或服務存取層級的流程⟧",
                             "⟦需要多項要素才能確認使用者或服務身分⟧"]) + ','),
    (" e:", ' e:' + js(E243) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦The ability to use the same credentials to access multiple resources and applications from different providers⟧",
                                     "⟦The process of identifying the access level of a user or service⟧",
                                     "⟦Requires several elements to identify a user or service⟧"]) + ','),
    ("     e:", '     e:' + js(EN243) + '}},'),
])

save(L)
print("批次 D 完成：#180 #187 #202 #224 #243")
