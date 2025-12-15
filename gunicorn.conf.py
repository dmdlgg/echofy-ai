"""
Configuração do Gunicorn para produção do Echofy AI
"""
import multiprocessing
import os

# Endereço e porta
bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"

# Workers
# Recomendação: 2-4 x número de cores da CPU
workers = int(os.getenv('WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Tipo de worker
# sync: para aplicações bloqueantes (padrão)
# gevent/eventlet: para aplicações assíncronas
worker_class = "sync"

# Threads por worker (para lidar com múltiplas requisições)
threads = int(os.getenv('THREADS', 2))

# Timeout
# Tempo máximo para processar uma requisição
timeout = int(os.getenv('TIMEOUT', 120))

# Keep alive
# Tempo que a conexão fica aberta após a resposta
keepalive = int(os.getenv('KEEPALIVE', 5))

# Número máximo de requisições antes de reiniciar o worker
# Previne memory leaks
max_requests = int(os.getenv('MAX_REQUESTS', 1000))
max_requests_jitter = int(os.getenv('MAX_REQUESTS_JITTER', 50))

# Logging
accesslog = "-"  # Log para stdout
errorlog = "-"   # Erros para stderr
loglevel = os.getenv('LOG_LEVEL', 'info')
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Preload app
# Carrega a aplicação antes de fazer fork dos workers
# Economiza memória RAM
preload_app = True

# Graceful timeout
# Tempo para workers finalizarem requisições antes de serem forçados a parar
graceful_timeout = int(os.getenv('GRACEFUL_TIMEOUT', 30))

# Worker temporary directory
# Útil para ambientes com sistema de arquivos read-only
worker_tmp_dir = "/dev/shm" if os.path.exists("/dev/shm") else None
