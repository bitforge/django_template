# Docker container startup
# Uses uvicorn because it's lightning-fast
import os
import sys
import uvicorn
import time


SRC_DIR = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, SRC_DIR)


def main():
    tic = time.perf_counter()
    from {{ project_name }}.asgi import application
    toc = time.perf_counter()
    print(f"Startup time: {toc - tic:0.4f}s")
    print('Running at http://0.0.0.0:8080/')

    try:
        uvicorn.run(
            application,
            host="0.0.0.0",
            port=8080,
            log_level='warning',
            lifespan='off',
            limit_concurrency=80,
        )
    except KeyboardInterrupt:
        return


if __name__ == "__main__":
    main()
