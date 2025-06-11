from typing import Callable, TypeAlias


ValidationFnT: TypeAlias = Callable[[object], bool]


class ValidationMixin:
    def is_optional(self) -> bool:
        self._is_optional = getattr(self, "_is_optional", False)
        return self._is_optional
   
    def set_optional(self, to: bool) -> None:
        self._is_optional = to

    def set_validation_trigger(self, fn) -> None:
        self._validation_trigger = fn

    def register_validation_func(self, fn: ValidationFnT) -> None:
        if not hasattr(self, "state"):
            raise RuntimeError("Base class does not inherit StyledWidget")
        if not hasattr(self, "_validation_trigger"):
            raise RuntimeError(
                "Tried to register validation function with no trigger"
            )
        self._validation_fn = fn
        self._validation_trigger.connect(self._validate_callback)
    
    def _validate_callback(self) -> None:
        data = self.serialize()
        if not data and self.is_optional():
            self.state.emit("")
            return
        self.state.emit(
            "" if self._validation_fn(data) else "error"
        )
    
    def is_valid(self) -> bool:
        data = self.serialize()
        if not data:
            return self.is_optional()
        if not hasattr(self, "_validation_fn"):
            return True
        return self._validation_fn(data)

    def serialize(self) -> object:
        raise NotImplementedError