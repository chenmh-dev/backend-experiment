from flask import Flask, g
from .utils import fail
from .exceptions import AppError

def register_error_handlers(app: Flask):

    @app.errorhandler(AppError)
    def handle_app_error(err: AppError):
        rid = getattr(g, "request_id", "-")
        app.logger.warning(
            f"AppError code={err.code} status={err.status} message={err.message}",
            extra={"request_id": rid}
        )
        return fail(code=err.code, message=err.message, status=err.status)
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(err: Exception):
        rid = getattr(g, "request_id", "-")
        # exception() 会自动带堆栈
        app.logger.exception("Unhandled exception", extra={"request_id": rid})
        
        import traceback
        traceback.print_exc()
        # 生产更建议记录日志，这里先保证契约稳定
        return fail(code="INTERNAL_ERROR", message="Internal server error", status=500)