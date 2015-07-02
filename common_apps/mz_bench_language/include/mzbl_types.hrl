-type abstract_expr() :: term().
-type meta() :: [{Key :: atom(), Value :: any()}].
-type script_value() :: term().
-type script_expr() :: tuple() | script_value().
-type script_loopspec() :: [tuple()].
-type script_validation_result() :: ok | {invalid_script, [string()]}.
-type pool() :: {[script_expr()], [tuple()]}.
-type named_pool() :: {atom(), [script_expr()], [tuple()]}.

-record(operation, {
        is_std = true :: true | false,
        name = undefined :: atom(),
        args = [] :: abstract_expr(),
        meta = [] :: meta()
        }).
-type operation() :: #operation{}.

-record(constant, {
        value = undefined :: term(),
        units = undefined :: atom(),
        meta = [] :: meta()
        }).
-type constant() :: #constant{}.

-record(ramp, {
        curve_type = linear :: linear,
        from :: #constant{},
        to :: #constant{},
        meta = [] :: meta()
        }).
-type ramp() :: #ramp{}.

-record(install_spec, {
        repo :: string(),
        branch :: string(),
        dir :: string()
        }).
-type install_spec() :: #install_spec{}.