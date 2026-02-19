# Tech Debt Audit – Spring PetClinic
**Rol:** Staff Software Engineer  
**Proyecto:** project_enterprise_monolith_2026  
**Herramientas:** SonarCloud · PMD · GitHub Actions  
**Fecha:** Febrero 2026  

---

## 1. Resumen Ejecutivo

Como Staff Software Engineers a cargo de la modernización de Spring PetClinic, realizamos un análisis exhaustivo de deuda técnica utilizando SonarCloud y PMD integrados en nuestro pipeline de CI. El análisis reveló **21 issues de mantenibilidad** distribuidos en severidades Blocker, High, Medium, Low e Info, con una complejidad ciclomática total de **101** y complejidad cognitiva de **47**.

Identificamos los **3 archivos de mayor riesgo** dentro del módulo `owner`, que concentran la mayor complejidad y los issues más críticos del proyecto. A continuación se presenta el plan de refactoring priorizado usando el patrón **Strangler Fig**, que permite modernizar el sistema de forma gradual sin interrumpir la funcionalidad existente.

---

## 2. Métricas Generales del Proyecto (SonarCloud)

| Métrica | Valor | Evaluación |
|---|---|---|
| Cyclomatic Complexity Total | 101 | ⚠️ Alto — umbral recomendado ≤ 10 por método |
| Cognitive Complexity Total | 47 | ⚠️ Moderado |
| Total Issues | 21 | 🔴 Requiere atención |
| Blocker | 3 | 🔴 Crítico |
| High | 3 | 🔴 Alto |
| Medium | 9 | 🟡 Moderado |
| Low | 2 | 🟢 Bajo |
| Info | 4 | ℹ️ Informativo |
| Code Smells | 21 | ⚠️ Alto |
| Maintainability Rating | A | ✅ Aceptable |

---

## 3. Top 3 Hotspots Identificados

Los hotspots fueron seleccionados combinando dos criterios objetivos obtenidos directamente de SonarCloud:
- **Cyclomatic Complexity** (complejidad estructural del código)
- **Cognitive Complexity** (dificultad de comprensión para un desarrollador)
- **Issues reales** detectados por SonarCloud

---

### 🔥 Hotspot #1 — `PetController.java`
**Riesgo:** ALTO | **Impacto:** ALTO | **Prioridad:** 1

**Ubicación:** `src/main/java/org/springframework/samples/petclinic/owner/PetController.java`

**Métricas SonarCloud:**
| Métrica | Valor | Evaluación |
|---|---|---|
| Cyclomatic Complexity | **27** | 🔴 Más alto del módulo |
| Cognitive Complexity | **15** | 🔴 Más alto del módulo (empatado) |
| Issue detectado | L69: "Immediately return this expression instead of assigning it to the temporary variable 'owner'" | Code Smell – Low |

**Análisis técnico:**
`PetController.java` es el archivo con **mayor complejidad ciclomática del módulo** (27), lo que significa que tiene 27 caminos de ejecución posibles. Esto hace que sea extremadamente difícil de testear exhaustivamente y muy propenso a bugs en casos edge. El issue en L69 evidencia un patrón de código descuidado donde se asigna un valor a una variable temporal solo para retornarla inmediatamente, sin ninguna transformación intermedia. Este anti-patrón, aunque menor en aislamiento, indica una falta de atención al diseño limpio que se replica en todo el archivo.

**Plan Strangler Fig — 3 fases:**
```
Fase 1 (Sprint 1): Resolver issue y reducir complejidad inmediata
  → Eliminar variable temporal 'owner' en L69, retornar expresión directamente
  → Identificar todos los métodos con CC > 5 dentro del controller
  → Documentar flujos de ejecución actuales con diagramas

Fase 2 (Sprint 2): Extraer PetService
  → Crear interfaz PetService con lógica de negocio de mascotas
  → Mover validaciones y operaciones CRUD de Pet al service
  → PetController solo delega: objetivo CC ≤ 10 por método

Fase 3 (Sprint 3): Validar y estabilizar
  → Asegurar 80%+ de coverage en PetService
  → Verificar en SonarCloud reducción de CC de 27 → ≤ 12
  → Confirmar que Cognitive Complexity baje de 15 → ≤ 8
```

---

### 🔥 Hotspot #2 — `Owner.java`
**Riesgo:** ALTO | **Impacto:** ALTO | **Prioridad:** 2

**Ubicación:** `src/main/java/org/springframework/samples/petclinic/owner/Owner.java`

**Métricas SonarCloud:**
| Métrica | Valor | Evaluación |
|---|---|---|
| Cyclomatic Complexity | **22** | 🔴 Segundo más alto del módulo |
| Cognitive Complexity | **15** | 🔴 Más alto del módulo (empatado) |
| Issue detectado | L139: "Merge this if statement with the enclosing one" | Code Smell – Medium/Major |

**Análisis técnico:**
`Owner.java` presenta el **segundo mayor Cyclomatic Complexity (22)** y la **mayor Cognitive Complexity (15)** del módulo, compartida con `PetController.java`. El issue en L139 evidencia `if` statements anidados innecesariamente, lo cual aumenta tanto la complejidad estructural como la cognitiva del modelo. Más crítico aún es el problema arquitectónico de fondo: `Owner.java` es un **modelo anémico** que mezcla anotaciones JPA (`@Entity`, `@Column`), lógica de negocio y gestión de colecciones de `Pet` en una sola clase. Esto viola la separación de capas y hace que cualquier cambio en la base de datos impacte directamente en la lógica de negocio.

**Plan Strangler Fig — 3 fases:**
```
Fase 1 (Sprint 1): Resolver issue de if anidado
  → Fusionar if statements en L139: if (condA && condB) { ... }
  → Mapear todas las responsabilidades actuales de Owner.java
  → Resultado: issue Medium resuelto, reducción de Cognitive Complexity

Fase 2 (Sprint 2): Separar capas de dominio y persistencia
  → Crear OwnerEntity: solo anotaciones JPA y mapeo de BD
  → Crear OwnerDomain: lógica de negocio pura sin anotaciones JPA
  → OwnerService: mapea entre OwnerEntity y OwnerDomain

Fase 3 (Sprint 3): Migrar referencias y deprecar Owner.java
  → Actualizar todos los consumers de Owner.java progresivamente
  → Verificar reducción de CC de 22 → ≤ 10 en SonarCloud
  → Asegurar 0 regresión en tests existentes
```

---

### 🔥 Hotspot #3 — `OwnerController.java`
**Riesgo:** MEDIO | **Impacto:** ALTO | **Prioridad:** 3

**Ubicación:** `src/main/java/org/springframework/samples/petclinic/owner/OwnerController.java`

**Métricas SonarCloud:**
| Métrica | Valor | Evaluación |
|---|---|---|
| Cyclomatic Complexity | **21** | 🟡 Tercero más alto del módulo |
| Cognitive Complexity | **7** | 🟡 Moderado |
| Issue detectado | L80: "Define a constant instead of duplicating this literal 'error' 3 times" | Code Smell – High/Critical |

**Análisis técnico:**
Aunque `OwnerController.java` tiene el **tercer mayor Cyclomatic Complexity (21)**, su issue es el más severo en términos de calidad: el literal `"error"` aparece duplicado 3 veces violando el principio **DRY (Don't Repeat Yourself)**. Cualquier cambio en este string requiere modificar 3 lugares distintos, aumentando el riesgo de inconsistencias y bugs. Con CC de 21, el controller también asume demasiadas responsabilidades: CRUD de owners, búsqueda por apellido y orquestación de vistas, violando el principio de **Single Responsibility (SRP)**.

**Plan Strangler Fig — 3 fases:**
```
Fase 1 (Sprint 1): Eliminar duplicación — resolver issue crítico
  → Definir constante: private static final String VIEW_OWNER_FORM = "error"
  → Reemplazar las 3 ocurrencias del literal por la constante
  → Resultado: issue High/Critical de SonarCloud eliminado

Fase 2 (Sprint 2): Extraer OwnerService
  → Crear interfaz OwnerService con métodos: findOwner(), saveOwner(), searchByLastName()
  → Mover lógica de negocio del controller al service
  → Controller solo delega: objetivo CC ≤ 8

Fase 3 (Sprint 3): Cobertura y validación final
  → Tests unitarios para OwnerService con 80%+ coverage
  → Verificar en SonarCloud reducción CC de 21 → ≤ 8
  → 0 issues High o Critical en OwnerController
```

---

## 4. Matriz de Priorización por Riesgo/Impacto

| # | Archivo | CC | Cognitive C. | Issue Real | Severidad | Riesgo | Impacto | Prioridad |
|---|---|---|---|---|---|---|---|---|
| 1 | `PetController.java` | **27** | **15** | Variable temporal innecesaria – L69 | Low | 🔴 Alto | 🔴 Alto | **1** |
| 2 | `Owner.java` | **22** | **15** | If anidado innecesario – L139 | Medium/Major | 🔴 Alto | 🔴 Alto | **2** |
| 3 | `OwnerController.java` | **21** | **7** | Literal duplicado 3 veces – L80 | High/Critical | 🟡 Medio | 🔴 Alto | **3** |

> **Nota de priorización:** `PetController.java` tiene prioridad 1 por tener la mayor Cyclomatic Complexity (27), lo que representa el mayor riesgo de introducir bugs al hacer cambios. `Owner.java` es prioridad 2 por su problema arquitectónico de fondo (modelo anémico) que tiene el mayor impacto a largo plazo.

---

## 5. ¿Por qué el patrón Strangler Fig?

El patrón **Strangler Fig** es la estrategia de modernización más adecuada para este monolito porque:

- **No interrumpe la funcionalidad existente:** cada fase extrae funcionalidad gradualmente mientras el sistema sigue operando
- **Reduce el riesgo de regresión:** los cambios son incrementales y verificables en cada sprint
- **Es medible:** SonarCloud y PMD confirman objetivamente si la complejidad bajó tras cada fase
- **Escala al equipo:** un equipo de 2 personas puede ejecutar las fases de forma paralela

**Alternativas descartadas:**
- **Big Bang Rewrite:** riesgo extremadamente alto para un equipo pequeño, no recomendado
- **Branch by Abstraction:** mayor overhead de coordinación para el alcance actual del proyecto

---

## 6. Reducción Esperada de Deuda Técnica

| Métrica | Antes | Después (estimado) | Reducción |
|---|---|---|---|
| Cyclomatic Complexity Total | 101 | ~65 | ~35% |
| Cognitive Complexity Total | 47 | ~30 | ~36% |
| Issues High/Critical | 3 | 0 | 100% |
| Issues Medium | 9 | ~3 | ~67% |

