# -*- coding: utf-8 -*-
"""核對原文 批次 A：#46 #61 #80 #82 #94（PDF 第 14、18、24、25、28 頁）。
   一次性腳本，保留供追溯。"""
import io, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vfy import load, save, patch, js, arr, arr2

L = load()

# ── #46（PDF 第 14 頁）───────────────────────────────────────────────
# 原文是「Azure virtual machines:」「Azure SQL databases:」兩個標籤各接一個下拉，
# 不是完整句子；把 sent 改成標籤形式，問句照原文。
patch(L, 46, """Question #46  ·  Topic 1  ·  HOTSPOT
Which cloud deployment solution is used for Azure virtual machines and Azure SQL databases? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.
Hot Area:

Answer Area
Azure virtual machines:　▼　Infrastructure as a service (IaaS) ｜ Platform as a service (PaaS) ｜ Software as a service (SaaS)
Azure SQL databases:　▼　Infrastructure as a service (IaaS) ｜ Platform as a service (PaaS) ｜ Software as a service (SaaS)

紅框標出的正解
1. Azure virtual machines　→　Infrastructure as a service (IaaS)
2. Azure SQL databases　→　Platform as a service (PaaS)

（核對來源：PDF 第 14 頁）""", line_edits=[
    (" q:", ' q:"Azure 虛擬機器與 Azure SQL Database 使用的是哪一種雲端部署解決方案？請在答案區選出正確的選項。",'),
    (" sent:", ' sent:' + js("⟦Azure 虛擬機器⟧：{0}\n⟦Azure SQL Database⟧：{1}") + ','),
    (" en:{q:", ' en:{q:"Which cloud deployment solution is used for Azure virtual machines and Azure SQL databases? To answer, select the appropriate options in the answer area.",'),
    ("     sent:", '     sent:' + js("⟦Azure virtual machines⟧: {0}\n⟦Azure SQL databases⟧: {1}") + ','),
])

# ── #61（PDF 第 18 頁）───────────────────────────────────────────────
# 原文的答案區描述沒有引號，反推時多加了「」/ ''，拿掉。
patch(L, 61, """Question #61  ·  Topic 1  ·  DRAG DROP
Match the cloud model to the correct advantage.
Instructions: To answer, drag the appropriate cloud model from the column on the left to its advantage on the right. Each cloud model may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point
Select and Place:

Cloud model：Hybrid Cloud ｜ Private Cloud ｜ Public Cloud

Work Area（紅框標出的正解順序）
1. No required capital expenditure.　→　Public Cloud
2. Provides complete control over security.　→　Private Cloud
3. Provides a choice to use on-premises or cloud-based resources.　→　Hybrid Cloud

（核對來源：PDF 第 18 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦不需要資本支出⟧", "⟦提供對安全性的完整控制⟧", "⟦可以選擇使用地端或雲端資源⟧"]) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦No required capital expenditure⟧", "⟦Provides complete control over security⟧", "⟦Provides a choice to use on-premises or cloud-based resources⟧"]) + ','),
], text_subs=[
    ("【「不需要資本支出」】", "【不需要資本支出】"),
    ("【「提供對安全性的完整控制」】", "【提供對安全性的完整控制】"),
    ("【「可以選擇使用地端或雲端資源」】", "【可以選擇使用地端或雲端資源】"),
    ("['No required capital expenditure']", "[No required capital expenditure]"),
    ("['Provides complete control over security']", "[Provides complete control over security]"),
    ("['Provides a choice to use on-premises or cloud-based resources']", "[Provides a choice to use on-premises or cloud-based resources]"),
])

# ── #80（PDF 第 24 頁）───────────────────────────────────────────────
# 原文的描述是完整句「Resources can be provisioned…」，不是「Scalability means that…」；
# 第一版拆題時補上的「指的是 / means that」拿掉。
patch(L, 80, """Question #80  ·  Topic 1  ·  DRAG DROP
Match the cloud computing benefits to the correct descriptions.
To answer, drag the appropriate benefit from the column on the left to its description on the right. Each benefit may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Benefits：Agility ｜ Geo-distribution ｜ Scalability

Answer Area（紅框標出的正解順序）
1. Resources can be provisioned dynamically to meet changing demands.　→　Scalability
2. Applications and data can be deployed to multiple regions.　→　Geo-distribution
3. Applications can be developed, tested, and launched rapidly.　→　Agility

（核對來源：PDF 第 24 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦可以動態佈建資源，以因應變動的需求⟧", "⟦應用程式與資料可以部署到多個區域⟧", "⟦應用程式可以快速開發、測試並上線⟧"]) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Resources can be provisioned dynamically to meet changing demands⟧", "⟦Applications and data can be deployed to multiple regions⟧", "⟦Applications can be developed, tested, and launched rapidly⟧"]) + ','),
], text_subs=[
    ("【指的是可以動態佈建資源，以因應變動的需求】", "【可以動態佈建資源，以因應變動的需求】"),
    ("【指的是應用程式與資料可以部署到多個區域】", "【應用程式與資料可以部署到多個區域】"),
    ("【指的是應用程式可以快速開發、測試並上線】", "【應用程式可以快速開發、測試並上線】"),
    ("[means that resources can be provisioned dynamically to meet changing demands]", "[Resources can be provisioned dynamically to meet changing demands]"),
    ("[means that applications and data can be deployed to multiple regions]", "[Applications and data can be deployed to multiple regions]"),
    ("[means that applications can be developed, tested, and launched rapidly]", "[Applications can be developed, tested, and launched rapidly]"),
])

# ── #82（PDF 第 25 頁）───────────────────────────────────────────────
# 兩個下拉在原文都是 IaaS / PaaS / SaaS 同一個順序，答案是 PaaS、IaaS；
# 反推時把 App1 那格的選項順序搬動過，改回原文順序並重對 a。
SVC = ["基礎結構即服務（IaaS）", "平台即服務（PaaS）", "軟體即服務（SaaS）"]
SVC_EN = ["Infrastructure as a service (IaaS)", "Platform as a service (PaaS)", "Software as a service (SaaS)"]
patch(L, 82, """Question #82  ·  Topic 1  ·  HOTSPOT
You plan to use Azure to host two apps named App1 and App2. The apps must meet the following requirements:
➯ You must be able to modify the code of App1.
➯ Administrative effort to manage the operating system of App1 must be minimized.
➯ App2 must run interactively with the operating system of the server.
Which type of cloud service should you use for each app? To answer, select the appropriate options in the answer area.
NOTE: Each correct selection is worth one point.
Hot Area:

Answer Area
App1:　▼　Infrastructure as a service (IaaS) ｜ Platform as a service (PaaS) ｜ Software as a service (SaaS)
App2:　▼　Infrastructure as a service (IaaS) ｜ Platform as a service (PaaS) ｜ Software as a service (SaaS)

紅框標出的正解
1. App1　→　Platform as a service (PaaS)
2. App2　→　Infrastructure as a service (IaaS)

（核對來源：PDF 第 25 頁）""", line_edits=[
    (" sent:", ' sent:' + js("App1：{0}\nApp2：{1}") + ','),
    (" dd:[", ' dd:' + arr2([SVC, SVC]) + ','),
    (" a:[", ' a:[1,0],'),
    ("     sent:", '     sent:' + js("App1: {0}\nApp2: {1}") + ','),
    ("     dd:[", '     dd:' + arr2([SVC_EN, SVC_EN]) + ','),
], text_subs=[
    ("\\nSelect the type of cloud service to use for each app.",
     "\\nWhich type of cloud service should you use for each app? To answer, select the appropriate options in the answer area."),
])

# ── #94（PDF 第 28 頁）───────────────────────────────────────────────
patch(L, 94, """Question #94  ·  Topic 1  ·  DRAG DROP
Match the cloud computing benefits to the appropriate descriptions.
To answer, drag the appropriate benefit from the column on the left to its description on the right. Each benefit may be used once, more than once, or not at all.
NOTE: Each correct match is worth one point.
Select and Place:

Benefits：Disaster recovery ｜ Geo-distribution ｜ High availability ｜ Scalability

Answer Area（紅框標出的正解順序）
1. Increase the compute capacity of apps in the cloud.　→　Scalability
2. Provide a continuous user experience with no apparent downtime.　→　High availability
3. Ensure that users always have the best experience by deploying apps to all the regions where there are users.　→　Geo-distribution

（核對來源：PDF 第 28 頁）""", line_edits=[
    (" tgt:[", ' tgt:' + arr(["⟦提高雲端應用程式的運算容量⟧", "⟦提供連續的使用者體驗，讓使用者感覺不到停機⟧", "⟦把應用程式部署到所有有使用者的區域，確保使用者永遠得到最佳體驗⟧"]) + ','),
    ("     tgt:[", '     tgt:' + arr(["⟦Increase the compute capacity of apps in the cloud⟧", "⟦Provide a continuous user experience with no apparent downtime⟧", "⟦Ensure that users always have the best experience by deploying apps to all the regions where there are users⟧"]) + ','),
], text_subs=[
    ("【指的是提高雲端應用程式的運算容量】", "【提高雲端應用程式的運算容量】"),
    ("【指的是提供連續的使用者體驗，讓使用者感覺不到停機】", "【提供連續的使用者體驗，讓使用者感覺不到停機】"),
    ("【指的是把應用程式部署到所有有使用者的區域，確保使用者永遠得到最佳體驗】", "【把應用程式部署到所有有使用者的區域，確保使用者永遠得到最佳體驗】"),
    ("[means that you can increase the compute capacity of apps in the cloud]", "[Increase the compute capacity of apps in the cloud]"),
    ("[means that you can provide a continuous user experience with no apparent downtime]", "[Provide a continuous user experience with no apparent downtime]"),
    ("[means that you can ensure that users always have the best experience by deploying apps to all the regions where there are users]", "[Ensure that users always have the best experience by deploying apps to all the regions where there are users]"),
])

save(L)
print("批次 A 完成：#46 #61 #80 #82 #94")
