package com.backtester.backtester.dto;

import java.time.LocalDate;

public record BacktestRequest(
        String prompt,
        String ticker,
        LocalDate startDate,
        LocalDate endDate
) {}