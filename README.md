Descripción del proyecto

Este proyecto tiene como objetivo desarrollar un sistema de recomendación para una plataforma de e-commerce, enfocado en identificar relaciones de complementariedad entre categorías de productos y aprovechar dichas relaciones para fomentar la venta cruzada (cross-selling).

A partir del análisis de datos transaccionales, se busca no solo recomendar productos que los clientes suelen comprar juntos, sino también priorizar aquellos que contribuyen al aumento del valor de compra (ticket promedio).


Problema de negocio

La plataforma no cuenta con un sistema de recomendación que sugiera productos complementarios entre categorías relacionadas, lo que limita las oportunidades de venta cruzada y el incremento del ticket promedio.


Análisis Exploratorio (EDA)

Durante el EDA se identificaron los siguientes hallazgos clave:

La mayoría de los pedidos contienen un solo producto → oportunidad de cross-selling
Existen diferencias significativas en el valor promedio entre categorías
Se identificaron patrones de co-compra entre grupos de productos
Algunas categorías presentan mayor potencial para aumentar el ticket promedio

Estos resultados permitieron justificar la construcción de un sistema de recomendación basado en relaciones entre categorías.


Metodología

El desarrollo del proyecto se dividió en las siguientes etapas:

1. Preparación de datos (ETL)
integración de múltiples fuentes (orders, products, payments, reviews, customers)
limpieza de datos (nulos, duplicados)
creación del dataset consolidado (df_model)
agrupación de categorías en segmentos estratégicos
2. Ingeniería de características
construcción de relaciones de co-ocurrencia entre categorías
cálculo de frecuencia de compra conjunta
incorporación del valor económico (ticket promedio por grupo)
normalización de variables
3. Modelado

Se desarrollaron dos modelos:

 - Modelo 1 – Baseline (Reglas)
basado en frecuencia de co-ocurrencia
incorpora valor económico del grupo recomendado
genera un ranking de recomendaciones
alta interpretabilidad
 - Modelo 2 – Machine Learning (Random Forest)
clasifica combinaciones de categorías como frecuentes o no
utiliza variables económicas como predictor
permite capturar patrones más complejos


Resultados
Accuracy modelo ML: 0.66
Recall clase positiva: 1.00
F1-score: 0.73
Interpretación:
el modelo identifica todas las combinaciones relevantes
prioriza la cobertura de recomendaciones
es funcional como un MVP


Insights clave
Existen patrones claros de compra conjunta entre categorías
No todas las combinaciones son igual de valiosas
El valor económico debe ser considerado en la recomendación
Es preferible recomendar de más que perder oportunidades de venta


Conclusión

El sistema desarrollado permite generar recomendaciones de productos complementarios basadas en datos reales de compra, integrando criterios de frecuencia y valor económico.

El modelo es funcional, interpretable y adecuado como un primer MVP, demostrando el potencial del uso de analítica de datos para mejorar la experiencia del usuario y aumentar los ingresos en plataformas de e-commerce.


Tecnologías utilizadas
Python
Pandas
NumPy
Scikit-learn
Matplotlib / Seaborn
