% function returning csv data for symbol

-module(csv).
-compile(export_all).
% -export([csvData/1, test/0]).

-import(eredis, [start_link/0, q/1]).


csvData(Symbol) ->
   {ok, C} = eredis:start_link(),
   % {ok, Test} = eredis:q(C, ["GET", "foo"]),
   {ok, Count} = eredis:q(C, ["ZCARD", "MSFT"]),
   Count.