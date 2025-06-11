from typing import Callable, TypeAlias


ValidationFnT: TypeAlias = Callable[[object], bool]


class ValidationMixin:
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
        self.state.emit(
            "" if self._validation_fn(self.serialize()) else "error"
        )
    
    def is_valid(self) -> bool:
        if not hasattr(self, "_validation_fn"):
            return True
        return self._validation_fn(self.serialize())

    def serialize(self) -> object:
        raise NotImplementedError