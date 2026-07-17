package com.backtester.backtester.dto;

public record PythonEngineResponse(
        Double totalReturn,
        Double sharpeRatio,
        Double maxDrawdown,
        String equityCurveJson
) {}