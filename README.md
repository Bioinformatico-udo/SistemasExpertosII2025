# Sistemas Expertos II 2025

## 📋 Descripción del Proyecto
Repositorio principal para el desarrollo de sistemas expertos por grupos.

## 🏗️ Estructura del Proyecto
/
├── docs/ # Documentación general
├── grupos/ # Aquí vivirán las aplicaciones de cada grupo
│ ├── grupo1/
│ ├── grupo2/
│ ├── grupo3/
│ ├── grupo4/
│ └── grupo5/
├── scripts/ # Scripts de utilidad común
├── tests/ # Pruebas de integración
└── .github/ # Configuración de GitHub

## 🚀 Grupos de Desarrollo
| Grupo | Rama | Estado | Responsable |
|-------|------|--------|-------------|
| 1 | `Grupo1` | Activo | - |
| 2 | `Grupo2` | Activo | - |
| 3 | `Grupo3` | Activo | - |
| 4 | `Grupo4` | Activo | - |
| 5 | `Grupo5` | Activo | - |

## 📌 Políticas del Repositorio
- **main**: Rama protegida, solo integración vía Pull Request
- **Ramas de grupo**: Cada equipo trabaja en su rama asignada
- **Commits**: Usar conventional commits

## 🛠️ Cómo Contribuir
Ver [CONTRIBUTING.md](docs/CONTRIBUTING.md) para guías detalladas.
"@ | Out-File -FilePath README.md -Encoding UTF8

# 3. Crear archivo de contribución
@"
# Guía de Contribución

## 🌳 Estructura de Ramas
- `main` - Rama principal (protegida)
- `Grupo1` al `Grupo5` - Ramas de desarrollo por equipo

## 📝 Convención de Commits
Formato: `<tipo>(<alcance>): <descripción>`

**Tipos:**
- `feat`: Nueva funcionalidad
- `fix`: Corrección de errores
- `docs`: Documentación
- `style`: Formato, estilo
- `refactor`: Refactorización
- `test`: Pruebas
- `chore`: Mantenimiento

**Ejemplos:**
feat(grupo1): agregar motor de inferencia básico
fix(grupo2): corregir conexión a base de datos
docs(grupo3): actualizar README con instrucciones

## 🔄 Flujo de Trabajo

### Para Grupos:
1. Trabajar en su rama asignada (`GrupoX`)
2. Hacer commits con mensajes descriptivos
3. Actualizar su rama regularmente

### Para Integrar a main:
1. Crear Pull Request desde rama de grupo hacia main
2. Esperar revisión del coordinador
3. Resolver comentarios si los hay
4. ¡Fusionar cuando esté aprobado!

## ✅ Checklist antes de PR
- [ ] El código funciona correctamente
- [ ] Se han probado los cambios
- [ ] La documentación está actualizada
- [ ] Los commits siguen la convención
"@ | Out-File -FilePath docs/CONTRIBUTING.md -Encoding UTF8

# 4. Crear archivo para cada grupo (placeholder)
1..5 | ForEach-Object {
    $grupo = "grupo$_"
    New-Item -ItemType Directory -Path "grupos/$grupo" -Force
    
    @"
# Grupo $_ - [Nombre del Proyecto]

## 📁 Estructura de la Aplicación
Colocar aquí el código de la aplicación.

## 🚀 Cómo Ejecutar

## 👥 Integrantes
- 
- 

## 📅 Estado Actual
- 
"@ | Out-File -FilePath "grupos/$grupo/README.md" -Encoding UTF8
}

# 5. Crear configuración de GitHub Actions
@"
name: Validar Pull Request

on:
  pull_request:
    branches: [ main ]

jobs:
  validate-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Verificar estructura básica
        run: |
          echo "✅ Pull Request válido"
          # Aquí se pueden agregar validaciones específicas
          
      - name: Notificar al coordinador
        run: |
          echo "PR de \${{ github.actor }} listo para revisión"
"@ | Out-File -FilePath ".github/workflows/validate.yml" -Encoding UTF8

# 6. Crear script de utilidad para integración
@"
#!/bin/bash
# Script para integrar ramas de grupos a main

echo "📦 Integrando ramas de grupos a main"
echo "===================================="

# Lista de grupos
grupos=("Grupo1" "Grupo2" "Grupo3" "Grupo4" "Grupo5")

for grupo in "\${grupos[@]}"; do
    echo ""
    echo "🔍 Procesando \$grupo..."
    
    # Verificar si la rama existe
    if git show-ref --verify --quiet "refs/remotes/origin/\$grupo"; then
        echo "✅ Rama \$grupo encontrada"
        
        # Crear rama local si no existe
        if ! git show-ref --verify --quiet "refs/heads/\$grupo-local"; then
            git checkout -b "\$grupo-local" "origin/\$grupo"
            echo "   Creada rama local \$grupo-local"
        fi
    else
        echo "⚠️ Rama \$grupo no encontrada en remoto"
    fi
done

echo ""
echo "✅ Proceso completado"
"@ | Out-File -FilePath "scripts/integrar-grupos.sh" -Encoding UTF8
