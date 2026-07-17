package com.backtester.backtester.controller;

import com.backtester.backtester.dto.BacktestRequest;
import com.backtester.backtester.entity.TradingStrategy;
import com.backtester.backtester.service.BacktestService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/v1/backtests")
@CrossOrigin(origins = "*") // Allows connections from our frontend server smoothly
public class BacktestController {

    private final BacktestService backtestService;

    public BacktestController(BacktestService backtestService) {
        this.backtestService = backtestService;
    }

    @PostMapping("/run")
    public ResponseEntity<TradingStrategy> runBacktest(@RequestBody BacktestRequest request) {
        TradingStrategy completedStrategy = backtestService.initiateBacktest(request);
        return ResponseEntity.ok(completedStrategy);
    }
}