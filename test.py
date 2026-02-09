#!/usr/bin/env python3
"""
Script de prueba para verificar que todo funciona correctamente
"""

import sys
import os

def test_imports():
    """Verifica que todas las dependencias estén instaladas"""
    print("🧪 Verificando dependencias...")

    required = {
        'flask': 'Flask',
        'flask_cors': 'Flask-CORS',
        'torch': 'PyTorch',
        'safetensors': 'SafeTensors',
        'soundfile': 'SoundFile',
        'numpy': 'NumPy'
    }

    failed = []
    for module, name in required.items():
        try:
            __import__(module)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NO INSTALADO")
            failed.append(name)

    if failed:
        print(f"\n❌ Faltan dependencias: {', '.join(failed)}")
        print("   Ejecuta: pip install -r requirements.txt")
        return False

    print("\n✅ Todas las dependencias instaladas\n")
    return True


def test_model():
    """Verifica que el modelo esté descargado"""
    print("🧪 Verificando modelo Voxtral...")

    model_dir = os.environ.get('VOXTRAL_MODEL_DIR', 'voxtral-model')
    required_files = [
        'consolidated.safetensors',
        'tekken.json',
        'params.json'
    ]

    if not os.path.exists(model_dir):
        print(f"  ✗ Directorio {model_dir} no existe")
        print("\n❌ Modelo no descargado")
        print("   Ejecuta: ./download_model.sh")
        return False

    missing = []
    for file in required_files:
        path = os.path.join(model_dir, file)
        if os.path.exists(path):
            size = os.path.getsize(path)
            print(f"  ✓ {file} ({size / (1024**3):.2f} GB)")
        else:
            print(f"  ✗ {file} - NO ENCONTRADO")
            missing.append(file)

    if missing:
        print(f"\n❌ Faltan archivos: {', '.join(missing)}")
        print("   Ejecuta: ./download_model.sh")
        return False

    print("\n✅ Modelo Voxtral listo\n")
    return True


def test_backend():
    """Verifica que el backend pueda importarse"""
    print("🧪 Verificando backend...")

    sys.path.insert(0, 'backend')

    try:
        import voxtral_inference
        print("  ✓ voxtral_inference.py")
    except Exception as e:
        print(f"  ✗ voxtral_inference.py - {e}")
        return False

    try:
        import server
        print("  ✓ server.py")
    except Exception as e:
        print(f"  ✗ server.py - {e}")
        return False

    print("\n✅ Backend correcto\n")
    return True


def test_frontend():
    """Verifica que los archivos del frontend existan"""
    print("🧪 Verificando frontend...")

    required_files = [
        'frontend/index.html',
        'frontend/css/style.css',
        'frontend/js/app.js',
        'frontend/manifest.json',
        'frontend/sw.js',
        'standalone.html'
    ]

    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - NO ENCONTRADO")
            missing.append(file)

    if missing:
        print(f"\n❌ Faltan archivos: {', '.join(missing)}")
        return False

    print("\n✅ Frontend completo\n")
    return True


def main():
    print("=" * 50)
    print("  VoxTral PWA - Test Suite")
    print("=" * 50)
    print()

    tests = [
        ('Dependencias', test_imports),
        ('Modelo', test_model),
        ('Backend', test_backend),
        ('Frontend', test_frontend)
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ Error en test {name}: {e}\n")
            results.append((name, False))

    print("=" * 50)
    print("  Resumen")
    print("=" * 50)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {name}")

    print()

    all_pass = all(result for _, result in results)

    if all_pass:
        print("🎉 ¡Todos los tests pasaron!")
        print()
        print("Puedes iniciar el servidor:")
        print("  python backend/server.py")
        print()
        print("O usa la versión standalone:")
        print("  open standalone.html")
        return 0
    else:
        print("⚠️  Algunos tests fallaron")
        print()
        print("Revisa los errores arriba y:")
        print("  1. Instala dependencias: pip install -r requirements.txt")
        print("  2. Descarga modelo: ./download_model.sh")
        return 1


if __name__ == '__main__':
    sys.exit(main())
