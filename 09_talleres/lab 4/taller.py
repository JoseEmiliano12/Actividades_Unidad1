import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# ---------- EJERCICIO 1: Operaciones difusas ----------
alto = 0.8
pesado = 0.4

print("--- EJERCICIO 1: OPERACIONES DIFUSAS ---")
print("OR  (unión):        ", max(alto, pesado))
print("AND (intersección): ", min(alto, pesado))
print("NOT (complemento):  ", round(1 - alto, 2))

# ---------- EJERCICIO 2: Inferencia difusa (propina) ----------
# Variables lingüísticas
comida   = ctrl.Antecedent(np.arange(0, 11, 1), 'comida')
servicio = ctrl.Antecedent(np.arange(0, 11, 1), 'servicio')
propina  = ctrl.Consequent(np.arange(0, 26, 1), 'propina')

comida.automf(names=['mala', 'regular', 'buena'])
servicio.automf(names=['mala', 'regular', 'buena'])

propina['baja']  = fuzz.trimf(propina.universe, [0, 0, 13])
propina['media'] = fuzz.trimf(propina.universe, [0, 13, 25])
propina['alta']  = fuzz.trimf(propina.universe, [13, 25, 25])

# Reglas SI-ENTONCES
r1 = ctrl.Rule(servicio['mala'] | comida['mala'], propina['baja'])
r2 = ctrl.Rule(servicio['regular'], propina['media'])
r3 = ctrl.Rule(servicio['buena'] | comida['buena'], propina['alta'])

sistema = ctrl.ControlSystemSimulation(ctrl.ControlSystem([r1, r2, r3]))

# Caso de prueba inicial
sistema.input['comida'] = 6.5
sistema.input['servicio'] = 9.8
sistema.compute()

print("\n--- EJERCICIO 2: CASO PRINCIPAL ---")
print("Propina sugerida:", round(sistema.output['propina'], 2), "%")

# Mostrar gráfico
propina.view(sim=sistema)
plt.savefig("propina.png")
plt.show()

# ---------- RETO: Los 4 casos de la tabla ----------
print("\n--- RETO OPCIONAL: TABLA DE EVALUACIÓN ---")
print("Comida | Servicio | Propina")
print("-" * 28)
for c, s in [(2, 3), (5, 5), (9, 9), (2, 9)]:
    prueba = ctrl.ControlSystemSimulation(ctrl.ControlSystem([r1, r2, r3]))
    prueba.input['comida'] = c
    prueba.input['servicio'] = s
    prueba.compute()
    print(f"  {c:^4} |   {s:^6} | {prueba.output['propina']:.2f} %")