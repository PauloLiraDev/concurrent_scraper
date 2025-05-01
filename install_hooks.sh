#!/bin/bash
# filepath: /home/paulo-lira/Projects/concurrent_scraper/install_hooks.sh

echo "⚙️ Installing git hooks for Concurrent Scraper..."

# Criar diretório .git/hooks se não existir
mkdir -p .git/hooks

# Copiar o hook pre-push
cp pre-push .git/hooks/

# Tornar o hook executável
chmod +x .git/hooks/pre-push

# Verificar se a instalação foi bem-sucedida
if [ -x .git/hooks/pre-push ]; then
  echo "✅ Git pre-push hook instalado com sucesso!"
  echo "🔍 O hook será executado automaticamente antes de cada push para verificar:"
  echo "   - Formatação de código (black)"
  echo "   - Lint checks (ruff)"
  echo "   - Testes unitários"
  echo "   - Testes de integração"
else
  echo "❌ Falha ao instalar o pre-push hook."
  exit 1
fi

# Instruções adicionais
echo ""
echo "📝 Nota: Para pular a verificação em um push específico, use a flag --no-verify:"
echo "   git push --no-verify"
echo ""