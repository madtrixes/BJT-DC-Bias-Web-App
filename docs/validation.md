# Lab 03: Browser Acceptance Validation (Cases A1–A5)

| กรณี | เลือกโหมดและกรอกค่า | คาดหมายก่อนรัน | เห็นจริง | วิธีตรวจ | สถานะ |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **A1 · โหมดเดิม** | Divider · R₁ = 100 kΩ, R₂ = 22 kΩ, R₈ = 1 kΩ | ผลต้องตรงกับเมื่อรัน Lab 2 ก่อนแก้ และเทียบได้กับค่าอ้างอิงเดิม<br>I_C ≈ 1.23 mA · V_CE ≈ 8.05 V | I_C = 1.23 mA, V_CE = 8.05 V | Playwright MCP | PASS |
| **A2 · Fixed** | Fixed · R_B = 1 MΩ | คำนวณได้โดยไม่ต้องกรอก R_E<br>I_C ≈ 1.13 mA · V_CE ≈ 9.51 V | I_C = 1.13 mA, V_CE = 9.51 V | Playwright MCP | PASS |
| **A3 · Emitter** | Emitter · R_B = 1 MΩ, R_E = 1 kΩ | มีช่องและใช้ค่า R_E<br>I_C ≈ 1.03 mA · V_CE ≈ 8.71 V | I_C = 1.03 mA, V_CE = 8.71 V | Playwright MCP | PASS |
| **A4 · เปลี่ยนค่าเดียว** | Emitter · เหมือน A3 แต่เปลี่ยน R_E เป็น 2 kΩ | ทำนายก่อนรันว่า I_C จะลดลงจาก A3 พร้อมเหตุผลสั้น ๆ<br>I_C ≈ 0.94 mA · V_CE ≈ 8.03 V | I_C = 0.94 mA, V_CE = 8.03 V | Playwright MCP | PASS |
| **A5 · อินพุตผิด** | Fixed · R_B = 0 | มีข้อความให้แก้ R_B เว็บไม่ล่ม และไม่แสดงผลเดิมเป็นผลของรอบนี้ | แสดงข้อความแจ้งเตือน Error ถูกต้อง | Playwright MCP | PASS |
