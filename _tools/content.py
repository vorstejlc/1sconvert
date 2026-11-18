"""Phase 2 SEO content for 1sconvert.com.
Inserts a guide, conversion tables and an FAQ (plus FAQPage JSON-LD) into each page
between <!-- content:start/end --> and <!-- jsonld:start/end --> markers. Re-runnable.
Usage (from the repo root): python _tools/content.py
"""
import sys, os, re, json, html, math

SITE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def f(x, sig=6):
    """Format a number: up to `sig` significant figures, thousands separators, no trailing zeros."""
    if x == 0: return '0'
    a = abs(x)
    if a >= 1e15 or a < 1e-6:
        m, e = f'{x:.4e}'.split('e'); return f'{float(m):g} × 10^{int(e)}'.replace('^', '<sup>').replace(' × 10<sup>', ' × 10<sup>') + '</sup>'
    d = max(0, sig - 1 - int(math.floor(math.log10(a))))
    s = f'{x:,.{d}f}'
    if '.' in s: s = s.rstrip('0').rstrip('.')
    return s

def table(head, rows):
    th = ''.join(f'<th>{h}</th>' for h in head)
    tr = '\n'.join('<tr>' + ''.join(f'<td{" class=\"txt\"" if (i == 0 and isinstance(c, str) and not re.match(r'^[-−\d.,]', c)) else ""}>{c}</td>' for i, c in enumerate(r)) + '</tr>' for r in rows)
    return f'<div class="tbl-scroll"><table class="data"><thead><tr>{th}</tr></thead><tbody>\n{tr}\n</tbody></table></div>'

def strip_tags(s): return re.sub(r'<[^>]+>', '', s)

PAGES = {}

# ───────────────────────── FORCE ─────────────────────────
LBF, KGF, GF = 4.4482216, 9.80665, 0.00980665
PAGES['force'] = dict(
 guide_h='How to convert force units',
 guide=f"""
<p>Force is a push or pull on an object. The SI unit is the <strong>newton (N)</strong>, the force that accelerates a 1 kg mass at 1 m/s². In the US, engineers use the <strong>pound-force (lbf)</strong>. Older metric drawings and spring or load specifications often use the <strong>kilogram-force (kgf)</strong>, the weight of 1 kg under standard gravity (9.80665 m/s²).</p>
<ul>
<li><strong>Newtons to lbf:</strong> multiply by 0.224809 (1 N = 0.2248 lbf)</li>
<li><strong>lbf to newtons:</strong> multiply by 4.44822 (1 lbf = 4.448 N)</li>
<li><strong>kgf to newtons:</strong> multiply by 9.80665</li>
<li><strong>kN to lbf:</strong> multiply by 224.809</li>
<li><strong>gf to lbf:</strong> divide by 453.592 (1 gf = 0.0022046 lbf)</li>
<li><strong>Dyne to newtons:</strong> divide by 100,000</li>
</ul>
<p>Related: convert force per area on the <a href="pressure.html">pressure converter</a>, or mass on the <a href="weight.html">weight converter</a>.</p>""",
 tables=[
  ('Newtons to pound-force and kilogram-force', table(['N', 'lbf', 'kgf', 'kN'],
     [[f(n), f(n/LBF), f(n/KGF), f(n/1000)] for n in [1, 5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000, 10000]])),
  ('Pound-force to newtons', table(['lbf', 'N', 'kN', 'kgf'],
     [[f(n), f(n*LBF), f(n*LBF/1000), f(n*LBF/KGF)] for n in [1, 5, 10, 25, 50, 100, 250, 500, 1000, 5000]])),
 ],
 faq=[
  ("How many newtons are in a pound-force?", "One pound-force equals 4.448 newtons (4.4482216 N). To convert lbf to N, multiply by 4.448. For example, 50 lbf = 222.4 N."),
  ("How do I convert newtons to lbf?", "Multiply newtons by 0.2248, or divide by 4.448. For example, 100 N = 22.48 lbf and 1 kN = 224.8 lbf."),
  ("What is the difference between kg and kgf?", "A kilogram (kg) is a unit of mass. A kilogram-force (kgf) is a unit of force: the weight of 1 kg under standard gravity, 9.80665 N. A 10 kg object weighs about 98.1 N, or 10 kgf, on Earth."),
  ("How do I convert gf to lbf?", "One gram-force is 0.0022046 lbf, so divide grams-force by 453.592. For example, 500 gf = 1.102 lbf."),
  ("How many kN is a tonne-force?", "One metric tonne-force (1,000 kgf) is 9.80665 kN. As a rule of thumb, 1 kN is roughly the weight of a 102 kg mass."),
  ("What is a dyne?", "The dyne is the CGS unit of force: the force that accelerates 1 gram at 1 cm/s². One dyne is 0.00001 N, so 1 N = 100,000 dyn."),
 ])

# ───────────────────────── POWER ─────────────────────────
HP, PS, BTUH = 745.69987, 735.49875, 0.29307107
PAGES['power'] = dict(
 guide_h='How to convert power units',
 guide="""
<p>Power is the rate at which energy is used or work is done. One <strong>watt (W)</strong> is one joule per second. Electric motors and appliances are rated in watts or kilowatts, engines in <strong>horsepower</strong>, and heating and air-conditioning equipment often in <strong>BTU per hour</strong>.</p>
<p>There are two common horsepowers. <strong>Mechanical (imperial) horsepower</strong> is 550 ft·lbf/s, or 745.7 W. <strong>Metric horsepower</strong> (PS, CV or pk) is 75 kgf·m/s, or 735.5 W, about 1.4% smaller. European car brochures usually quote PS.</p>
<ul>
<li><strong>kW to hp:</strong> multiply by 1.341</li>
<li><strong>hp to kW:</strong> multiply by 0.7457</li>
<li><strong>kW to PS:</strong> multiply by 1.360</li>
<li><strong>BTU/h to watts:</strong> multiply by 0.2931 (12,000 BTU/h ≈ 3.517 kW, one ton of cooling)</li>
<li><strong>Watts to BTU/h:</strong> multiply by 3.412</li>
</ul>
<p>Related: <a href="energy.html">energy converter</a> (kWh, joules, BTU) and <a href="refrigeration.html">refrigeration calculator</a> (tons of refrigeration, COP and EER).</p>""",
 tables=[
  ('Standard motor sizes: kW to horsepower', table(['kW', 'hp (mechanical)', 'PS (metric hp)', 'BTU/h'],
     [[f(k), f(k*1000/HP, 4), f(k*1000/PS, 4), f(k*1000/BTUH, 5)] for k in [0.37, 0.75, 1.1, 1.5, 2.2, 3, 4, 5.5, 7.5, 11, 15, 18.5, 22, 30, 37, 45, 55, 75, 90, 110, 132, 160, 200, 250]])),
  ('Horsepower to kilowatts', table(['hp', 'kW', 'PS', 'W'],
     [[f(h), f(h*HP/1000, 5), f(h*HP/PS, 5), f(h*HP, 6)] for h in [1, 2, 5, 10, 25, 50, 75, 100, 150, 200, 250, 300, 400, 500, 1000]])),
 ],
 faq=[
  ("How many watts are in a horsepower?", "One mechanical horsepower is 745.7 W. One metric horsepower (PS) is 735.5 W."),
  ("How do I convert kW to hp?", "Multiply kilowatts by 1.341 to get mechanical horsepower. For example, 100 kW = 134.1 hp, and a 7.5 kW motor is about 10 hp."),
  ("What is the difference between hp and PS?", "PS (Pferdestärke) is metric horsepower, defined as 75 kgf·m/s = 735.5 W. Mechanical horsepower is 745.7 W, so 1 hp = 1.014 PS. European cars are usually rated in PS; US and UK figures usually use hp."),
  ("How do I convert BTU/h to watts?", "Multiply BTU per hour by 0.2931. For example, a 12,000 BTU/h air conditioner is 3.517 kW of cooling, and 9,000 BTU/h is 2.64 kW."),
  ("What is the difference between kW and kWh?", "A kilowatt (kW) is a rate of power. A kilowatt-hour (kWh) is an amount of energy: power multiplied by time. A 2 kW heater running for 3 hours uses 6 kWh."),
 ])

# ───────────────────────── TIME ─────────────────────────
YEAR = 31556952
def hms(s):
    h, r = divmod(int(s), 3600); m, sec = divmod(r, 60); return f'{h}:{m:02d}:{sec:02d}'
PAGES['time'] = dict(
 guide_h='How time units are defined',
 guide=f"""
<p>The SI unit of time is the <strong>second</strong>. Fixed units build on it: a minute is 60 s, an hour 3,600 s, a day 86,400 s and a week 604,800 s.</p>
<p>Months and years vary in length, so this converter uses <strong>Gregorian calendar averages</strong>. A year is 365.2425 days (31,556,952 s), which averages in the leap years. A month is one twelfth of that, 30.436875 days. For a specific calendar year, use 365 days (31,536,000 s), or 366 days (31,622,400 s) for a leap year.</p>
<ul>
<li><strong>Seconds to minutes:</strong> divide by 60</li>
<li><strong>Seconds to hours:</strong> divide by 3,600</li>
<li><strong>Milliseconds to seconds:</strong> divide by 1,000</li>
<li><strong>Days to hours:</strong> multiply by 24</li>
<li><strong>Weeks to days:</strong> multiply by 7</li>
</ul>""",
 tables=[
  ('How long each unit is', table(['Unit', 'Seconds', 'Minutes', 'Hours', 'Days'],
     [[n, f(s, 9), f(s/60, 8), f(s/3600, 8), f(s/86400, 7)] for n, s in [
       ('Minute', 60), ('Hour', 3600), ('Day', 86400), ('Week', 604800), ('Month (average)', YEAR/12),
       ('Year (365 days)', 31536000), ('Leap year (366 days)', 31622400), ('Year (Gregorian average)', YEAR),
       ('Decade (average)', YEAR*10), ('Century (average)', YEAR*100)]])),
  ('Seconds to minutes and hours', table(['Seconds', 'Minutes', 'Hours', 'h:mm:ss'],
     [[f(s), f(s/60, 5), f(s/3600, 5), hms(s)] for s in [30, 45, 60, 90, 100, 120, 180, 300, 500, 600, 900, 1000, 1800, 3600, 5400, 7200, 10000, 43200, 86400, 100000]])),
 ],
 faq=[
  ("How many seconds are in a day?", "There are 86,400 seconds in a day: 24 hours × 60 minutes × 60 seconds."),
  ("How many seconds are in a year?", "A common 365-day year has 31,536,000 seconds and a leap year has 31,622,400. The average Gregorian year, used by this converter, is 31,556,952 seconds."),
  ("How many weeks are in a year?", "A year has 52.14 weeks (365 ÷ 7), or 52.18 weeks on the Gregorian average of 365.2425 days. That is 52 full weeks plus 1 or 2 days."),
  ("How many days are in a month on average?", "The average month is 30.44 days (365.2425 ÷ 12). Calendar months range from 28 to 31 days."),
  ("How many hours are in a year?", "A 365-day year has 8,760 hours and a leap year has 8,784. The Gregorian average is 8,765.82 hours."),
  ("How do I convert milliseconds to seconds?", "Divide milliseconds by 1,000. For example, 2,500 ms = 2.5 s. To go from seconds to milliseconds, multiply by 1,000."),
 ])

# ───────────────────────── DENSITY ─────────────────────────
LBFT3 = 16.01846
MATS = [('Air (20 °C, sea level)', 1.204), ('Petrol / gasoline', 740), ('Ethanol', 789), ('Diesel fuel', 832), ('Olive oil', 911),
        ('Ice (0 °C)', 917), ('Fresh water (20 °C)', 998.2), ('Fresh water (4 °C)', 1000), ('Seawater', 1025), ('Milk', 1030),
        ('Concrete', 2400), ('Glass', 2500), ('Aluminium', 2700), ('Steel', 7850), ('Copper', 8960), ('Lead', 11340),
        ('Mercury (20 °C)', 13546), ('Gold', 19300)]
PAGES['density'] = dict(
 guide_h='How to convert density units',
 guide="""
<p>Density is mass per unit volume. The SI unit is <strong>kilograms per cubic metre (kg/m³)</strong>. Laboratories usually work in <strong>grams per cubic centimetre (g/cm³)</strong>, which is the same as g/mL, kg/L and tonnes per m³. US engineering uses <strong>pounds per cubic foot (lb/ft³)</strong>.</p>
<ul>
<li><strong>g/cm³ to kg/m³:</strong> multiply by 1,000</li>
<li><strong>kg/m³ to g/cm³:</strong> divide by 1,000</li>
<li><strong>lb/ft³ to kg/m³:</strong> multiply by 16.018</li>
<li><strong>kg/m³ to lb/ft³:</strong> multiply by 0.062428</li>
<li><strong>lb/in³ to g/cm³:</strong> multiply by 27.68</li>
</ul>
<p><strong>Specific gravity</strong> (relative density) is a material's density divided by the density of water. Because water is about 1,000 kg/m³, a specific gravity of 0.8 means about 800 kg/m³, or 0.8 g/cm³.</p>
<p>Related: <a href="weight.html">weight converter</a> and <a href="volume.html">volume converter</a>.</p>""",
 tables=[
  ('Density of common materials', table(['Material', 'kg/m³', 'g/cm³', 'lb/ft³'],
     [[n, f(d, 6), f(d/1000, 4), f(d/LBFT3, 4)] for n, d in MATS])
   + '<p class="note">Typical values. Actual density varies with temperature, pressure, composition and grade.</p>'),
 ],
 faq=[
  ("How do I convert g/cm³ to kg/m³?", "Multiply by 1,000. For example, aluminium at 2.70 g/cm³ is 2,700 kg/m³. To go the other way, divide kg/m³ by 1,000."),
  ("How do I convert lb/ft³ to kg/m³?", "Multiply pounds per cubic foot by 16.018. For example, 62.4 lb/ft³ (water) is about 1,000 kg/m³, and 150 lb/ft³ (concrete) is about 2,400 kg/m³."),
  ("What is the density of water?", "Pure water is about 1,000 kg/m³ (1 g/cm³ or 62.4 lb/ft³). It is densest at 4 °C (999.97 kg/m³) and slightly lighter at 20 °C (998.2 kg/m³). Seawater is about 1,025 kg/m³."),
  ("Is g/mL the same as g/cm³?", "Yes. One millilitre is exactly one cubic centimetre, so 1 g/mL = 1 g/cm³ = 1 kg/L = 1,000 kg/m³."),
  ("What is the difference between density and specific gravity?", "Density has units, such as kg/m³. Specific gravity has no units: it is the ratio of a material's density to that of water. Steel has a density of about 7,850 kg/m³ and a specific gravity of about 7.85."),
 ])

# ───────────────────────── ELECTRICITY ─────────────────────────
PREF = [('p', 'pico', '10<sup>−12</sup>', '0.000000000001', 'pF (capacitors)'),
        ('n', 'nano', '10<sup>−9</sup>', '0.000000001', 'nF, ns'),
        ('μ', 'micro', '10<sup>−6</sup>', '0.000001', 'μF, μA, μV'),
        ('m', 'milli', '10<sup>−3</sup>', '0.001', 'mA, mV, mΩ, mAh'),
        ('—', '(base unit)', '10<sup>0</sup>', '1', 'V, A, Ω, C, F'),
        ('k', 'kilo', '10<sup>3</sup>', '1,000', 'kV, kΩ, kA'),
        ('M', 'mega', '10<sup>6</sup>', '1,000,000', 'MΩ, MV'),
        ('G', 'giga', '10<sup>9</sup>', '1,000,000,000', 'GΩ')]
PAGES['electricity'] = dict(
 guide_h='Electrical units and prefixes',
 guide="""
<p>This converter covers five electrical quantities: <strong>voltage</strong> (volts, V), <strong>current</strong> (amperes, A), <strong>resistance</strong> (ohms, Ω), <strong>charge</strong> (coulombs, C, and amp-hours, Ah) and <strong>capacitance</strong> (farads, F). Within each quantity you are only moving between SI prefixes, such as milliamps to amps or kilohms to ohms.</p>
<p>You cannot convert directly <em>between</em> quantities, such as volts to amps. You need a second value and Ohm's law:</p>
<ul>
<li><code>V = I × R</code>: voltage equals current times resistance</li>
<li><code>I = V ÷ R</code> or <code>I = P ÷ V</code>: current from resistance or from power</li>
<li><code>P = V × I</code>: power in watts. For example, a 2,000 W kettle on 230 V draws about 8.7 A.</li>
</ul>
<p>Related: <a href="power.html">power converter</a> (W, kW, hp) and <a href="energy.html">energy converter</a> (Wh, kWh).</p>""",
 tables=[
  ('SI prefixes used in electronics', table(['Symbol', 'Prefix', 'Factor', 'Decimal', 'Examples'], [list(p) for p in PREF])),
  ('Battery capacity: mAh to Ah, coulombs and watt-hours', table(['mAh', 'Ah', 'Coulombs', 'Wh at 3.7 V', 'Wh at 5 V'],
     [[f(m), f(m/1000), f(m*3.6), f(m*3.7/1000, 4), f(m*5/1000, 4)] for m in [500, 1000, 2000, 2500, 3000, 4000, 5000, 10000, 20000, 26800]])
   + '<p class="note">3.7 V is the nominal voltage of a lithium-ion cell, and power banks are usually rated at this voltage. Many airlines allow power banks up to 100 Wh in carry-on luggage without approval.</p>'),
 ],
 faq=[
  ("How many milliamps are in an amp?", "There are 1,000 milliamps (mA) in one amp (A). To convert mA to A, divide by 1,000: 250 mA = 0.25 A."),
  ("How do I convert mAh to Wh?", "Multiply milliamp-hours by the voltage, then divide by 1,000: Wh = mAh × V ÷ 1,000. A 10,000 mAh power bank at 3.7 V holds 37 Wh."),
  ("Can I convert volts to amps?", "Not directly, because they measure different things. You also need the power or the resistance: amps = watts ÷ volts, or amps = volts ÷ ohms. For example, 1,000 W at 230 V is about 4.35 A."),
  ("How do I convert μF to nF?", "Multiply microfarads by 1,000. 0.1 μF = 100 nF = 100,000 pF, which is the value marked 104 on a ceramic capacitor."),
  ("How many ohms are in a kilohm?", "One kilohm (kΩ) is 1,000 ohms, so 4.7 kΩ = 4,700 Ω. One megohm (MΩ) is 1,000,000 Ω."),
  ("How many coulombs are in an amp-hour?", "One amp-hour is 3,600 coulombs: 1 A flowing for 3,600 seconds. One milliamp-hour is 3.6 C."),
 ])

# ───────────────────────── ENERGY ─────────────────────────
KWH, BTU, KCAL = 3.6e6, 1055.06, 4184
PAGES['energy'] = dict(
 guide_h='How to convert energy units',
 guide="""
<p>Energy is the capacity to do work. The SI unit is the <strong>joule (J)</strong>, the energy of 1 watt for 1 second. Different fields use different units:</p>
<ul>
<li>Electricity bills use the <strong>kilowatt-hour (kWh)</strong>: 1 kWh = 3.6 MJ</li>
<li>Food labels use the <strong>kilocalorie (kcal)</strong>, the "Calorie": 1 kcal = 4.184 kJ</li>
<li>Gas and heating in the US and UK use the <strong>BTU</strong>: 1 kWh = 3,412 BTU</li>
<li>Physics uses the <strong>electronvolt (eV)</strong>: 1 eV = 1.602 × 10<sup>−19</sup> J</li>
</ul>
<p><strong>Quick factors:</strong> kWh to MJ, multiply by 3.6. kcal to kJ, multiply by 4.184. BTU to kJ, multiply by 1.055. kWh to kcal, multiply by 860.4.</p>
<p>Energy is not the same as power. Power (W, kW) is the rate at which energy is used, and energy = power × time. See the <a href="power.html">power converter</a>.</p>""",
 tables=[
  ('Kilowatt-hours to MJ, BTU and kcal', table(['kWh', 'MJ', 'BTU', 'kcal'],
     [[f(k), f(k*KWH/1e6, 6), f(k*KWH/BTU, 6), f(k*KWH/KCAL, 6)] for k in [0.1, 0.5, 1, 2, 5, 10, 25, 50, 100, 250, 500, 1000]])),
  ('Food energy: kcal (Calories) to kilojoules', table(['kcal', 'kJ', 'Wh'],
     [[f(c), f(c*KCAL/1000, 5), f(c*KCAL/3600, 4)] for c in [50, 100, 150, 200, 250, 300, 400, 500, 750, 1000, 1500, 2000, 2500, 3000]])),
 ],
 faq=[
  ("How many joules are in a kWh?", "One kilowatt-hour is 3,600,000 joules (3.6 MJ): 1,000 W × 3,600 s."),
  ("What is the difference between calories and kcal?", "A food \"Calorie\" (capital C) is a kilocalorie: 1 kcal = 1,000 small calories = 4.184 kJ. A 2,000 kcal daily diet is about 8,368 kJ."),
  ("How do I convert kWh to BTU?", "Multiply kilowatt-hours by 3,412. For example, 10 kWh is about 34,121 BTU. To convert BTU to kWh, divide by 3,412."),
  ("What is the difference between kW and kWh?", "kW measures power, the rate of energy use. kWh measures energy used over time. A 2 kW heater running for 3 hours uses 6 kWh."),
  ("How many joules are in a calorie?", "One calorie (thermochemical) is 4.184 joules, so 1 kcal = 4,184 J."),
  ("How many kcal are in a kWh?", "One kilowatt-hour is about 860 kcal (3,600,000 J ÷ 4,184)."),
 ])

# ───────────────────────── LENGTH ─────────────────────────
IN, FT, MI = 0.0254, 0.3048, 1609.344
def ftin(cm):
    t = cm / 2.54; ft = int(t // 12); i = t - ft * 12
    return f"{ft}′ {i:.1f}″"
PAGES['length'] = dict(
 guide_h='How to convert length units',
 guide="""
<p>The SI unit of length is the <strong>metre (m)</strong>. Imperial and US units are defined exactly in metric terms: since 1959, one inch is exactly <strong>2.54 cm</strong>. That makes a foot 30.48 cm, a yard 0.9144 m and a mile 1,609.344 m.</p>
<ul>
<li><strong>Inches to cm:</strong> multiply by 2.54</li>
<li><strong>cm to inches:</strong> divide by 2.54 (or multiply by 0.3937)</li>
<li><strong>Feet to metres:</strong> multiply by 0.3048</li>
<li><strong>Metres to feet:</strong> multiply by 3.2808</li>
<li><strong>mm to inches:</strong> divide by 25.4</li>
<li><strong>km to miles:</strong> multiply by 0.62137</li>
<li><strong>Miles to km:</strong> multiply by 1.60934</li>
</ul>
<p>A <strong>nautical mile</strong> (1,852 m) is used at sea and in aviation; it is about 1.15 statute miles. Related: <a href="area.html">area converter</a> and <a href="speed.html">speed converter</a>.</p>""",
 tables=[
  ('Height: feet and inches to centimetres', table(['Height', 'Inches', 'cm', 'm'],
     [[f"{t//12}′ {t%12}″", str(t), f(t*2.54, 5), f(t*0.0254, 4)] for t in range(54, 81)])),
  ('Inches to centimetres', table(['Inches', 'cm', 'mm'],
     [[f(i), f(i*2.54, 5), f(i*25.4, 5)] for i in [0.25, 0.5, 0.75, 1, 2, 3, 4, 5, 6, 8, 10, 12, 18, 24, 36, 48]])),
  ('Kilometres to miles', table(['km', 'miles', 'm', 'ft'],
     [[f(k), f(k*1000/MI, 5), f(k*1000), f(k*1000/FT, 6)] for k in [1, 2, 3, 5, 10, 15, 20, 21.0975, 25, 42.195, 50, 100, 200, 500, 1000]])
   + '<p class="note">21.0975 km is a half marathon (13.1 mi) and 42.195 km a marathon (26.2 mi).</p>'),
 ],
 faq=[
  ("How many centimetres are in an inch?", "One inch is exactly 2.54 centimetres. To convert inches to cm, multiply by 2.54: 12 inches = 30.48 cm."),
  ("How do I convert my height to centimetres?", "Convert to total inches first (feet × 12 + inches), then multiply by 2.54. For example, 5′ 10″ is 70 inches = 177.8 cm."),
  ("How many feet are in a metre?", "One metre is 3.2808 feet, or 3 feet 3.37 inches. To convert metres to feet, multiply by 3.2808."),
  ("How do I convert km to miles?", "Multiply kilometres by 0.62137. A 10 km run is 6.21 miles. To go from miles to km, multiply by 1.609."),
  ("How do I convert mm to inches?", "Divide millimetres by 25.4. For example, 100 mm = 3.937 in, and 6 mm = 0.236 in."),
  ("What is the difference between a mile and a nautical mile?", "A statute mile is 1,609.344 m. A nautical mile is 1,852 m, based on one minute of latitude, and is used at sea and in aviation. One nautical mile is about 1.151 statute miles."),
 ])

# ───────────────────────── WEIGHT ─────────────────────────
LB, OZ, ST, TOZ = 0.45359237, 0.028349523125, 6.35029318, 0.0311034768
PAGES['weight'] = dict(
 guide_h='How to convert weight and mass',
 guide="""
<p>The SI unit of mass is the <strong>kilogram (kg)</strong>. The pound is defined exactly as <strong>0.45359237 kg</strong>, so every pound and ounce conversion is exact. The UK and Ireland often give body weight in <strong>stone</strong>: 1 stone = 14 lb = 6.35 kg.</p>
<ul>
<li><strong>kg to lbs:</strong> multiply by 2.20462</li>
<li><strong>lbs to kg:</strong> multiply by 0.453592 (or divide by 2.20462)</li>
<li><strong>Grams to ounces:</strong> divide by 28.3495</li>
<li><strong>Ounces to grams:</strong> multiply by 28.3495</li>
<li><strong>Stone to kg:</strong> multiply by 6.35029</li>
</ul>
<p>Precious metals use the <strong>troy ounce</strong> (31.1035 g), which is about 10% heavier than the ordinary (avoirdupois) ounce of 28.35 g. Related: <a href="cooking.html">cooking converter</a> and <a href="density.html">density converter</a>.</p>""",
 tables=[
  ('Kilograms to pounds', table(['kg', 'lb', 'lb + oz', 'stone + lb'],
     [[f(k), f(k/LB, 5), f"{int(k/LB)} lb {(k/LB - int(k/LB))*16:.1f} oz", f"{int(k/ST)} st {(k/LB) - int(k/ST)*14:.1f} lb"] for k in [1, 2, 5, 10, 20, 25, 30, 40, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 110, 120, 150]])),
  ('Pounds to kilograms', table(['lb', 'kg', 'g'],
     [[f(p), f(p*LB, 5), f(p*LB*1000, 6)] for p in [0.25, 0.5, 1, 2, 5, 10, 20, 25, 50, 100, 120, 140, 150, 160, 180, 200, 220, 250, 300]])),
  ('Grams to ounces', table(['g', 'oz', 'lb'],
     [[f(g), f(g/1000/OZ, 4), f(g/1000/LB, 4)] for g in [5, 10, 25, 50, 100, 125, 200, 250, 300, 400, 454, 500, 750, 1000]])),
 ],
 faq=[
  ("How many pounds are in a kilogram?", "One kilogram is 2.20462 pounds. To convert kg to lbs, multiply by 2.20462: 70 kg = 154.3 lb."),
  ("How do I convert lbs to kg?", "Multiply pounds by 0.453592, or divide by 2.20462. For example, 150 lb = 68.04 kg."),
  ("How many kg is a stone?", "One stone is 14 pounds, which is 6.35 kg. To convert stone and pounds to kg, work out total pounds (stone × 14 + pounds) and multiply by 0.4536. 11 st 4 lb = 158 lb = 71.7 kg."),
  ("How many grams are in an ounce?", "One ounce (avoirdupois) is 28.35 grams. A troy ounce, used for gold and silver, is 31.10 grams."),
  ("What is the difference between a metric ton, short ton and long ton?", "A metric tonne is 1,000 kg (2,204.6 lb). A US short ton is 2,000 lb (907.2 kg). A UK long ton is 2,240 lb (1,016 kg)."),
  ("Is weight the same as mass?", "Strictly, mass is measured in kilograms and weight is a force measured in newtons. In everyday use, \"weight\" means mass, and kg and lb are used for both. See the force converter for newtons."),
 ])

# ───────────────────────── TEMPERATURE ─────────────────────────
c2f = lambda c: c * 9 / 5 + 32
PAGES['temperature'] = dict(
 guide_h='Temperature conversion formulas',
 guide="""
<p>Unlike most units, temperature scales have different zero points, so you cannot convert with a single multiplication.</p>
<ul>
<li><strong>Celsius to Fahrenheit:</strong> <code>°F = °C × 9/5 + 32</code></li>
<li><strong>Fahrenheit to Celsius:</strong> <code>°C = (°F − 32) × 5/9</code></li>
<li><strong>Celsius to Kelvin:</strong> <code>K = °C + 273.15</code></li>
<li><strong>Fahrenheit to Rankine:</strong> <code>°R = °F + 459.67</code></li>
</ul>
<p><strong>Quick mental estimate:</strong> to get °F, double the Celsius value and add 30. For 20 °C that gives 70 °F; the exact value is 68 °F. The shortcut is close between about 0 and 30 °C.</p>
<p>A temperature <em>difference</em> converts without the offset: a change of 1 °C (or 1 K) equals a change of 1.8 °F. Related: <a href="cooking.html">oven temperatures</a> and the <a href="refrigeration.html">refrigerant PT chart</a>.</p>""",
 tables=[
  ('Celsius to Fahrenheit', table(['°C', '°F', 'K', 'Reference'],
     [[f(c), f(c2f(c), 5), f(c + 273.15, 6), n] for c, n in [(-273.15, 'Absolute zero'), (-40, '°C and °F are equal'), (-18, 'Home freezer'), (-10, ''), (0, 'Water freezes'),
       (4, 'Fridge'), (10, ''), (15, ''), (20, 'Room temperature'), (25, ''), (30, 'Hot day'), (35, ''), (37, 'Body temperature'), (40, 'Fever / heatwave'),
       (50, ''), (60, ''), (70, ''), (80, ''), (90, ''), (100, 'Water boils (sea level)'), (150, ''), (180, 'Moderate oven'), (200, 'Hot oven'), (250, '')]])),
  ('Fahrenheit to Celsius', table(['°F', '°C'],
     [[f(x), f((x - 32) * 5 / 9, 4)] for x in [-40, -4, 0, 10, 20, 32, 40, 50, 60, 68, 70, 72, 75, 80, 90, 98.6, 100, 110, 212, 300, 325, 350, 375, 400, 425, 450]])),
 ],
 faq=[
  ("How do I convert Celsius to Fahrenheit?", "Multiply by 9/5 (or 1.8) and add 32. For example, 25 °C × 1.8 + 32 = 77 °F."),
  ("How do I convert Fahrenheit to Celsius?", "Subtract 32, then multiply by 5/9. For example, (350 °F − 32) × 5/9 = 176.7 °C."),
  ("At what temperature are Celsius and Fahrenheit equal?", "−40 °C is exactly −40 °F, the only point where the two scales meet."),
  ("What is normal body temperature in Fahrenheit?", "37 °C is 98.6 °F. A fever is usually taken to start around 38 °C (100.4 °F)."),
  ("What is absolute zero?", "Absolute zero is 0 K, which is −273.15 °C or −459.67 °F. It is the lowest possible temperature."),
  ("Why is Kelvin written without a degree sign?", "Kelvin is an absolute scale and an SI base unit, so it is written as K, not °K. A difference of 1 K equals a difference of 1 °C."),
 ])

# ───────────────────────── SPEED ─────────────────────────
MPH, KN = 0.44704, 0.514444
PAGES['speed'] = dict(
 guide_h='How to convert speed units',
 guide="""
<p>Speed is distance per unit time. Science uses <strong>metres per second (m/s)</strong>. Road signs use <strong>km/h</strong> or <strong>mph</strong>. Ships and aircraft use <strong>knots</strong>, one nautical mile per hour.</p>
<ul>
<li><strong>km/h to mph:</strong> multiply by 0.62137</li>
<li><strong>mph to km/h:</strong> multiply by 1.60934</li>
<li><strong>m/s to km/h:</strong> multiply by 3.6</li>
<li><strong>km/h to m/s:</strong> divide by 3.6</li>
<li><strong>Knots to km/h:</strong> multiply by 1.852</li>
<li><strong>Knots to mph:</strong> multiply by 1.15078</li>
</ul>
<p><strong>Mach 1</strong> is the speed of sound: about 343 m/s (1,235 km/h) in air at 20 °C. It falls in colder air, so at airliner cruising altitude it is closer to 295 m/s. Related: <a href="length.html">length converter</a> and <a href="time.html">time converter</a>.</p>""",
 tables=[
  ('Speed limits: km/h to mph', table(['km/h', 'mph', 'm/s', 'knots'],
     [[f(k), f(k/3.6/MPH, 4), f(k/3.6, 4), f(k/3.6/KN, 4)] for k in [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 200, 250, 300]])),
  ('mph to km/h', table(['mph', 'km/h', 'm/s'],
     [[f(m), f(m*MPH*3.6, 4), f(m*MPH, 4)] for m in [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 100, 150, 200]])),
  ('Running pace and speed', table(['Pace per km', 'Pace per mile', 'km/h', 'mph'],
     [[f"{int(p)}:{int(round((p%1)*60)):02d}", f"{int(p*1.609344)}:{int(round((p*1.609344%1)*60)):02d}", f(60/p, 4), f(60/p/1.609344, 4)] for p in [3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 9, 10, 12]])),
 ],
 faq=[
  ("How do I convert km/h to mph?", "Multiply km/h by 0.6214. For example, 100 km/h = 62.1 mph and 50 km/h = 31.1 mph."),
  ("How do I convert mph to km/h?", "Multiply mph by 1.609. For example, 70 mph = 112.7 km/h and 30 mph = 48.3 km/h."),
  ("How do I convert m/s to km/h?", "Multiply metres per second by 3.6. For example, 10 m/s = 36 km/h. To go from km/h to m/s, divide by 3.6."),
  ("What is a knot?", "A knot is one nautical mile per hour: exactly 1.852 km/h, or about 1.151 mph. It is used for ships, aircraft and wind speed."),
  ("How fast is Mach 1?", "Mach 1 is the speed of sound: about 343 m/s, 1,235 km/h or 767 mph in air at 20 °C at sea level. It is lower in colder air, so it varies with altitude."),
  ("How fast is the speed of light?", "The speed of light in a vacuum is exactly 299,792,458 m/s, about 1.08 billion km/h or 671 million mph."),
 ])

# ───────────────────────── AREA ─────────────────────────
FT2, AC, MI2 = 0.09290304, 4046.8564224, 2589988.110336
PAGES['area'] = dict(
 guide_h='How to convert area units',
 guide="""
<p>Area is length × length, so area factors are the <em>square</em> of length factors. One foot is 0.3048 m, so one square foot is 0.3048² = 0.0929 m². The SI unit is the <strong>square metre (m²)</strong>. Land is usually measured in <strong>hectares</strong> (metric) or <strong>acres</strong> (US/UK).</p>
<ul>
<li><strong>m² to ft²:</strong> multiply by 10.7639</li>
<li><strong>ft² to m²:</strong> multiply by 0.092903 (or divide by 10.764)</li>
<li><strong>Hectares to acres:</strong> multiply by 2.47105</li>
<li><strong>Acres to hectares:</strong> multiply by 0.404686</li>
<li><strong>km² to square miles:</strong> multiply by 0.386102</li>
</ul>
<p>A <strong>hectare</strong> is a 100 m × 100 m square (10,000 m²). An <strong>acre</strong> is 43,560 ft², about 4,047 m² or roughly 64 m × 64 m. Related: <a href="length.html">length converter</a> and <a href="volume.html">volume converter</a>.</p>""",
 tables=[
  ('Floor area: square metres to square feet', table(['m²', 'ft²'],
     [[f(m), f(m/FT2, 6)] for m in [1, 5, 10, 12, 15, 20, 25, 30, 40, 50, 60, 75, 80, 100, 120, 150, 200, 250, 300, 500, 1000]])),
  ('Square feet to square metres', table(['ft²', 'm²'],
     [[f(x), f(x*FT2, 5)] for x in [10, 50, 100, 150, 200, 250, 500, 750, 1000, 1200, 1500, 1800, 2000, 2500, 3000, 4000, 5000, 10000]])),
  ('Land: acres and hectares', table(['Acres', 'Hectares', 'm²', 'ft²'],
     [[f(a), f(a*AC/1e4, 5), f(a*AC, 6), f(a*43560, 7)] for a in [0.1, 0.25, 0.5, 1, 2, 2.47105, 5, 10, 20, 40, 50, 100, 160, 640]])
   + '<p class="note">2.47105 acres = 1 hectare. 640 acres = 1 square mile (2.59 km²).</p>'),
 ],
 faq=[
  ("How do I convert square metres to square feet?", "Multiply by 10.764. For example, a 50 m² apartment is 538 ft², and 100 m² is 1,076 ft²."),
  ("How do I convert square feet to square metres?", "Multiply by 0.0929, or divide by 10.764. For example, 2,000 ft² is 185.8 m²."),
  ("How big is an acre?", "An acre is 43,560 square feet, or 4,046.86 m². That is about 0.405 hectares, or a square roughly 64 m (208 ft) on each side."),
  ("How many acres are in a hectare?", "One hectare is 2.471 acres. A hectare is 10,000 m², a square 100 m on each side."),
  ("How do I convert km² to square miles?", "Multiply square kilometres by 0.3861. One square mile is 2.59 km², or 640 acres."),
  ("Why can't I multiply area by the length conversion factor?", "Area has two dimensions, so the factor is squared. 1 m = 3.28 ft, but 1 m² = 3.28 × 3.28 = 10.76 ft²."),
 ])

# ───────────────────────── VOLUME ─────────────────────────
USG, UKG = 3.785411784, 4.54609
PAGES['volume'] = dict(
 guide_h='How to convert volume units',
 guide="""
<p>The SI unit of volume is the <strong>cubic metre (m³)</strong>. Everyday metric volume uses the <strong>litre</strong> (1 L = 1,000 cm³ = 0.001 m³) and the <strong>millilitre</strong> (1 mL = 1 cm³ = 1 cc).</p>
<p><strong>US and UK units are different.</strong> A US gallon is 3.785 L and a UK (imperial) gallon is 4.546 L, about 20% larger. A US pint is 473 mL and a UK pint is 568 mL. Even the fluid ounce differs: 29.57 mL (US) against 28.41 mL (UK).</p>
<ul>
<li><strong>Litres to US gallons:</strong> divide by 3.78541</li>
<li><strong>US gallons to litres:</strong> multiply by 3.78541</li>
<li><strong>Litres to UK gallons:</strong> divide by 4.54609</li>
<li><strong>mL to US fl oz:</strong> divide by 29.5735</li>
<li><strong>m³ to litres:</strong> multiply by 1,000</li>
</ul>
<p>Related: <a href="cooking.html">cooking converter</a> (cups and spoons) and <a href="density.html">density converter</a>.</p>""",
 tables=[
  ('Litres to gallons', table(['Litres', 'US gal', 'UK gal', 'US fl oz'],
     [[f(l), f(l/USG, 5), f(l/UKG, 5), f(l/USG*128, 5)] for l in [0.5, 1, 2, 4, 5, 10, 20, 25, 40, 50, 60, 75, 100, 200, 500, 1000]])),
  ('Gallons to litres', table(['Gallons', 'US gal → L', 'UK gal → L'],
     [[f(g), f(g*USG, 5), f(g*UKG, 5)] for g in [0.5, 1, 2, 3, 5, 10, 12, 15, 20, 25, 50, 55, 100]])),
  ('Millilitres to fluid ounces', table(['mL', 'US fl oz', 'UK fl oz'],
     [[f(m), f(m/1000/USG*128, 4), f(m/1000/UKG*160, 4)] for m in [5, 15, 30, 50, 100, 125, 150, 200, 250, 330, 355, 500, 700, 750, 1000]])),
 ],
 faq=[
  ("How many litres are in a gallon?", "A US gallon is 3.785 litres and a UK (imperial) gallon is 4.546 litres. Check which gallon is meant: fuel economy figures in the UK and US use different gallons."),
  ("How many mL are in a fluid ounce?", "A US fluid ounce is 29.57 mL and a UK fluid ounce is 28.41 mL. A 12 fl oz US can holds 355 mL."),
  ("How many cups are in a litre?", "One litre is 4.227 US cups (236.6 mL each), or 4 metric cups (250 mL each)."),
  ("How many litres are in a cubic metre?", "One cubic metre is exactly 1,000 litres. One litre is 1,000 cm³."),
  ("Is a cc the same as a mL?", "Yes. One cubic centimetre (cc or cm³) is exactly one millilitre. Engine sizes in cc are the same as millilitres: 1,600 cc = 1.6 L."),
  ("What is the difference between a US and UK pint?", "A US pint is 16 US fl oz (473 mL). A UK pint is 20 UK fl oz (568 mL), about 20% more."),
 ])

# ───────────────────────── PRESSURE ─────────────────────────
PSI, ATM, MMHG = 6894.757, 101325, 133.3224
PAGES['pressure'] = dict(
 guide_h='How to convert pressure units',
 guide="""
<p>Pressure is force per unit area. The SI unit is the <strong>pascal (Pa)</strong>, 1 N/m². It is very small, so engineering uses <strong>kPa</strong>, <strong>MPa</strong> and <strong>bar</strong> (1 bar = 100 kPa, close to atmospheric pressure). The US uses <strong>psi</strong>, pounds-force per square inch. Medicine uses <strong>mmHg</strong> for blood pressure, and weather maps use <strong>hPa</strong> or millibars, which are the same thing.</p>
<ul>
<li><strong>bar to psi:</strong> multiply by 14.5038</li>
<li><strong>psi to bar:</strong> multiply by 0.0689476</li>
<li><strong>psi to kPa:</strong> multiply by 6.89476</li>
<li><strong>kPa to psi:</strong> multiply by 0.145038</li>
<li><strong>atm to bar:</strong> multiply by 1.01325</li>
<li><strong>mmHg to kPa:</strong> multiply by 0.133322</li>
</ul>
<p><strong>Gauge vs absolute:</strong> tyre and refrigeration gauges read pressure <em>above</em> atmospheric (psig, bar g). Absolute pressure adds about 1.013 bar (14.7 psi) at sea level. Related: <a href="refrigeration.html">refrigerant PT chart</a> and <a href="force.html">force converter</a>.</p>""",
 tables=[
  ('bar to psi and kPa', table(['bar', 'psi', 'kPa', 'MPa'],
     [[f(b), f(b*1e5/PSI, 5), f(b*100, 6), f(b/10, 4)] for b in [0.1, 0.5, 1, 1.5, 2, 2.2, 2.5, 3, 4, 5, 6, 7, 8, 10, 12, 16, 20, 25, 50, 100, 200, 232, 300]])
   + '<p class="note">2.2–2.5 bar is a typical car tyre pressure; 200–232 bar is a full scuba cylinder.</p>'),
  ('psi to bar and kPa', table(['psi', 'bar', 'kPa'],
     [[f(p), f(p*PSI/1e5, 4), f(p*PSI/1000, 5)] for p in [1, 5, 10, 14.696, 20, 25, 30, 32, 35, 40, 50, 60, 80, 100, 120, 150, 200, 300, 500, 1000, 3000]])),
  ('Blood pressure: mmHg to kPa', table(['mmHg', 'kPa'],
     [[f(m), f(m*MMHG/1000, 3)] for m in [60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 180]])),
 ],
 faq=[
  ("How do I convert bar to psi?", "Multiply bar by 14.504. For example, 2.4 bar = 34.8 psi and 10 bar = 145 psi."),
  ("How do I convert psi to bar?", "Multiply psi by 0.06895, or divide by 14.504. For example, 32 psi = 2.21 bar."),
  ("What is 1 atmosphere in other units?", "One standard atmosphere is exactly 101,325 Pa: 101.325 kPa, 1.01325 bar, 14.696 psi or 760 mmHg."),
  ("What is the difference between psig and psia?", "psig is gauge pressure, measured relative to the surrounding air. psia is absolute pressure, measured from a perfect vacuum. At sea level, psia = psig + 14.7."),
  ("Are hPa and mbar the same?", "Yes. One hectopascal (hPa) equals one millibar (mbar) = 100 Pa. Standard sea-level air pressure is 1,013.25 hPa."),
  ("Are mmHg and Torr the same?", "They are almost identical. 1 Torr is 1/760 of an atmosphere (133.322 Pa), and 1 mmHg is 133.322 Pa. The difference is negligible for everyday use."),
 ])

# ───────────────────────── DATA ─────────────────────────
PAGES['data'] = dict(
 guide_h='Decimal vs binary data units',
 guide="""
<p>Data units come in two families, and mixing them up is the most common source of confusion.</p>
<ul>
<li><strong>Decimal (SI) units</strong> use powers of 1,000: 1 KB = 1,000 bytes, 1 MB = 1,000,000 bytes, 1 GB = 10<sup>9</sup> bytes. Storage makers, network speeds and macOS use these.</li>
<li><strong>Binary (IEC) units</strong> use powers of 1,024: 1 KiB = 1,024 bytes, 1 MiB = 1,048,576 bytes, 1 GiB = 1,073,741,824 bytes. Windows uses these but labels them "KB, MB, GB", which is why a new drive looks smaller than advertised.</li>
</ul>
<p><strong>Bits and bytes:</strong> 1 byte = 8 bits. Internet speeds are quoted in bits per second (Mbps, lowercase b). File sizes are in bytes (MB, uppercase B), so divide Mbps by 8 to get MB/s.</p>""",
 tables=[
  ('Why your drive shows less space than advertised', table(['Advertised', 'Bytes', 'Shown in Windows'],
     [[n, f(b, 15), (f(b/1024**3, 4) + ' GB') if b < 1024**4 else (f(b/1024**4, 4) + ' TB')] for n, b in [
       ('32 GB', 32e9), ('64 GB', 64e9), ('128 GB', 128e9), ('256 GB', 256e9), ('500 GB', 500e9), ('512 GB', 512e9),
       ('1 TB', 1e12), ('2 TB', 2e12), ('4 TB', 4e12), ('8 TB', 8e12), ('16 TB', 16e12)]])
   + '<p class="note">Windows divides by 1,024³ (GiB) or 1,024⁴ (TiB) but shows the result as "GB" or "TB". No space is missing.</p>'),
  ('Internet speed: Mbps to MB/s and download time', table(['Speed', 'MB/s', '1 GB file', '50 GB game'],
     [[f(m) + ' Mbps', f(m/8, 4), (lambda s: f"{int(s//3600)}h {int(s%3600//60):02d}m" if s >= 3600 else f"{int(s//60)}m {int(round(s%60)):02d}s")(8000/m), (lambda s: f"{int(s//3600)}h {int(s%3600//60):02d}m" if s >= 3600 else f"{int(s//60)}m {int(round(s%60)):02d}s")(400000/m)] for m in [10, 25, 50, 100, 200, 300, 500, 1000, 2500, 10000]])
   + '<p class="note">Ideal times at full line speed. Real downloads are usually slower because of protocol overhead and server limits.</p>'),
 ],
 faq=[
  ("How many MB are in a GB?", "In decimal units, 1 GB = 1,000 MB. In binary units, 1 GiB = 1,024 MiB. Storage makers use the decimal definition; Windows uses the binary one but labels it GB."),
  ("Why does my 1 TB drive show 931 GB?", "The drive holds 1,000,000,000,000 bytes. Windows divides by 1,024³ and shows 931 \"GB\" (really 931 GiB). No space is missing; it is a different unit."),
  ("How do I convert Mbps to MB/s?", "Divide megabits per second by 8. A 100 Mbps connection transfers at most 12.5 MB/s, so a 1 GB file takes about 80 seconds."),
  ("What is the difference between a bit and a byte?", "A bit is a single 0 or 1. A byte is 8 bits. Speeds use lowercase b (Mbps, bits); file sizes use uppercase B (MB, bytes)."),
  ("What is the difference between KB and KiB?", "1 KB (kilobyte) is 1,000 bytes. 1 KiB (kibibyte) is 1,024 bytes. The gap grows with size: 1 TiB is about 10% larger than 1 TB."),
 ])

# ───────────────────────── COOKING ─────────────────────────
CUP = 236.5882365
ING = [('Water', 237), ('Milk', 244), ('All-purpose flour', 120), ('Bread flour', 127), ('Granulated sugar', 200), ('Brown sugar (packed)', 213),
       ('Powdered / icing sugar', 113), ('Butter', 227), ('Honey', 340), ('Vegetable oil', 218), ('Rolled oats', 90), ('Cocoa powder', 85),
       ('Uncooked white rice', 185), ('Chopped nuts', 120), ('Chocolate chips', 170)]
PAGES['cooking'] = dict(
 guide_h='Cooking measurements explained',
 guide="""
<p>US recipes measure by volume (cups and spoons), while most other countries weigh ingredients in grams. Cup sizes also differ between countries:</p>
<ul>
<li><strong>US cup:</strong> 236.6 mL (often rounded to 240 mL on nutrition labels)</li>
<li><strong>Metric cup</strong> (UK, Australia, New Zealand, Canada): 250 mL</li>
<li><strong>Tablespoon:</strong> 14.8 mL (US) or 15 mL (metric). <strong>Australian tablespoon:</strong> 20 mL</li>
<li><strong>Teaspoon:</strong> 4.93 mL (US) or 5 mL (metric)</li>
</ul>
<p>Converting cups to grams depends on the ingredient: a cup of flour weighs about half as much as a cup of sugar. Use the table below for common ingredients. Related: <a href="weight.html">weight converter</a>, <a href="volume.html">volume converter</a> and <a href="temperature.html">temperature converter</a>.</p>""",
 tables=[
  ('Cups to grams for common ingredients', table(['Ingredient', '1 cup', '½ cup', '¼ cup', '1 tbsp'],
     [[n, f(g, 3) + ' g', f(g/2, 3) + ' g', f(g/4, 3) + ' g', f(g/16, 2) + ' g'] for n, g in ING])
   + '<p class="note">US cup, spooned and levelled. Typical values: weights vary with how the cup is filled, humidity and brand.</p>'),
  ('Butter: sticks, cups and grams', table(['US butter', 'Cups', 'Tbsp', 'Grams'],
     [[n, c, t, g] for n, c, t, g in [('½ stick', '¼', '4', '57 g'), ('1 stick', '½', '8', '113 g'), ('1½ sticks', '¾', '12', '170 g'),
       ('2 sticks', '1', '16', '227 g'), ('4 sticks (1 lb)', '2', '32', '454 g')]])),
 ],
 faq=[
  ("How many grams is a cup of flour?", "One US cup of all-purpose flour is about 120 g, spooned and levelled. Scooping straight from the bag packs it down and can give 140 g or more."),
  ("How many grams is a cup of sugar?", "One US cup of granulated sugar is about 200 g. Packed brown sugar is about 213 g, and powdered (icing) sugar about 113 g."),
  ("How many tablespoons are in a cup?", "There are 16 tablespoons in a US cup, and 48 teaspoons. A metric 250 mL cup is about 16.7 metric tablespoons."),
  ("Is a UK cup the same as a US cup?", "No. Recipes from the UK, Australia and New Zealand use a 250 mL metric cup. A US cup is 236.6 mL, about 5% smaller."),
  ("How many grams of butter are in a stick?", "One US stick of butter is 4 oz, 113 g or 8 tablespoons. One cup of butter is 2 sticks, or 227 g."),
  ("What is 180 °C in Fahrenheit for baking?", "180 °C is 356 °F, usually written as 350 °F (gas mark 4) in recipes. 200 °C is about 400 °F (gas mark 6)."),
 ])

# ───────────────────────── WRITE ─────────────────────────
def build(name, P):
    parts = [f'<section class="card info" id="guide">\n<h2>{P["guide_h"]}</h2>{P["guide"]}\n</section>']
    for i, (h, t) in enumerate(P['tables']):
        sid = ' id="tables"' if i == 0 else ''
        parts.append(f'<section class="card info"{sid}>\n<h2>{h}</h2>\n{t}\n</section>')
    faq = '\n'.join(f'<h3>{html.escape(q)}</h3>\n<p>{html.escape(a)}</p>' for q, a in P['faq'])
    parts.append(f'<section class="card info" id="faq">\n<h2>Frequently asked questions</h2>\n{faq}\n</section>')
    content = '<!-- content:start -->\n' + '\n'.join(parts) + '\n<!-- content:end -->\n'
    ld = {"@context": "https://schema.org", "@type": "FAQPage",
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in P['faq']]}
    jsonld = '<!-- jsonld:start -->\n<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=1) + '\n</script>\n<!-- jsonld:end -->\n'
    path = f'{SITE}/{name}.html'
    s = open(path, encoding='utf-8').read()
    s = re.sub(r'<!-- content:start -->.*?<!-- content:end -->\n', '', s, flags=re.S)
    s = re.sub(r'<!-- jsonld:start -->.*?<!-- jsonld:end -->\n', '', s, flags=re.S)
    assert s.count('</main>') == 1 and s.count('</head>') == 1, name
    s = s.replace('</main>', content + '</main>').replace('</head>', jsonld + '</head>')
    open(path, 'w', encoding='utf-8', newline='\n').write(s)
    words = len(strip_tags(content).split())
    print(f'{name}: +{words} words, {len(P["tables"])} tables, {len(P["faq"])} FAQs')

for n, P in PAGES.items(): build(n, P)
