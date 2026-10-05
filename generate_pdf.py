from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('DejaVu', 'B', 14)
        self.cell(0, 10, 'Переменные и расчетные формулы (index.html)', 0, 1, 'C')
        self.ln(5)

pdf = PDF()
pdf.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', uni=True)
pdf.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', uni=True)
pdf.set_font('DejaVu', '', 12)
pdf.add_page()

content = """
1. Переменные (исходные данные и константы):

Ppos — Посадочная нагрузка (Н)
Pvzl — Взлётная нагрузка (Н)
Ae — Эксплуатационная работа (Дж)
G0G — Отношение масс (G0 / Gпос)
Vpos — Посадочная скорость (км/ч)
Vvzl — Взлётная скорость (км/ч)
p0tire — Давление в колесе (10^6 Па)
eta — Коэффициент полноты диаграммы обжатия пневматика (η)
pmax — Максимальное давление в амортизаторе (МПа)
k — Показатель политропы (k)
Sam — Ход амортизатора (мм)
coef — Коэффициент начального давления
K — Коэффициент полноты работы амортизатора (K)
p0am — Начальное давление в амортизаторе (МПа)
deltab — Толщина стенки цилиндра (мм)
hzhmax — Максимальный уровень жидкости (мм)
Nkol — Число колёс
Lk, Lam — Плечи колёс и амортизатора (мм)

2. Расчётные формулы:

2.1. Интерполяция параметров колеса (Pмд, δмд, Aмд) по заданному давлению:
X = [(p0 - p2) * (X1 - X2) / (p1 - p2)] + X2

2.2. Максимальная работа (AmaxJ):
AmaxJ = Ae * G0G
(а также Amax = AmaxJ * 1000)

2.3. Коэффициенты для расчета усилия (C1, C2):
C1 = 0.5 * δмд * eta * Nkol / Pмд
ratio = Lk / Lam (передаточное отношение)
C2 = ratio * Sam * K * Nkol

2.4. Максимальное усилие на пневматик (Pпн) (через решение квадратного уравнения):
disc = C2^2 + 4 * C1 * Amax
Pпн = (-C2 + sqrt(disc)) / (2 * C1)

2.5. Максимальная перегрузка (ny):
ny = Pпн * Nkol / Ppos

2.6. Начальное усилие амортизатора (Pнач):
Pнач = coef * Ppos

2.7. Диаметр штока (dшт) и его площадь (Fшт):
dшт = 2 * sqrt(Pнач / (pi * p0am)) (затем округляется вверх до ближайшего чётного)
Fшт = pi * dшт^2 / 4

2.8. Наружный диаметр цилиндра (Dцил) и внутренняя площадь (Fцил):
Dцил = dшт + 2 * deltab
Fцил = pi * Dцил^2 / 4

2.9. Начальная высота газовой камеры (h0):
factor = 1 - (p0am / pmax)^(1/k)
h0 = (Fшт * Sam / (Fцил * factor)) (округляется вверх с шагом 10)

2.10. Ход газа (Δhгаза) и конечная высота (hmax):
Δhгаза = Fшт * Sam / Fцил
hmax = h0 - Δhгаза

2.11. Работа газа (Aгаза) и её доля (share):
V0 = Fцил * h0
Aгаза = (p0am * V0 / (k - 1)) * ((pmax / p0am)^((k - 1) / k) - 1) / 1000
share = (Aгаза / AmaxJ) * 100
"""

for line in content.strip().split('\n'):
    if line.strip().startswith('1.') or line.strip().startswith('2.'):
        pdf.set_font('DejaVu', 'B', 12)
    else:
        pdf.set_font('DejaVu', '', 12)
    pdf.multi_cell(0, 6, line)

pdf.output('formulas_and_variables.pdf')
