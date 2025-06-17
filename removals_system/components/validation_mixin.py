from typing import (
    Callable, TypeAlias, Self
)


ValidationFnT: TypeAlias = Callable[[object], bool]


class ValidationMixin:
    def is_optional(self) -> bool:
        self._is_optional = getattr(self, "_is_optional", False)
        return self._is_optional
   
    def set_optional(self, to: bool) -> Self:
        self._is_optional = to
        return self

    def set_validation_trigger(self, fn) -> Self:
        self._validation_trigger = fn
        return self

    def register_validation_func(self, fn: ValidationFnT) -> Self:
        if not hasattr(self, "state"):
            raise RuntimeError("Base class does not inherit StyledWidget")
        if not hasattr(self, "_validation_trigger"):
            raise RuntimeError(
                "Tried to register validation function with no trigger"
            )
        self._validation_fn = fn
        self._validation_trigger.connect(self._validate_callback)
        return self
    
    def _validate_callback(self) -> None:
        data = self.serialize()
        self.state: int
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