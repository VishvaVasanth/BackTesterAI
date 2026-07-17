package com.backtester.backtester.service;

import com.backtester.backtester.dto.BacktestRequest;
import com.backtester.backtester.dto.PythonEngineResponse;
import com.backtester.backtester.entity.TradingStrategy;
import com.backtester.backtester.repository.StrategyRepository;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

@Service
public class BacktestService {

    private final StrategyRepository strategyRepository;
    private final RestTemplate restTemplate;

    @Value("${python.engine.url}")
    private String pythonEngineUrl;

    public BacktestService(StrategyRepository strategyRepository, RestTemplate restTemplate) {
        this.strategyRepository = strategyRepository;
        this.restTemplate = restTemplate;
    }

    public TradingStrategy initiateBacktest(BacktestRequest request) {
        // 1. Prepare data payload to send to the Python microservice
        Map<String, Object> pythonPayload = Map.of(
                "prompt", request.prompt(),
                "ticker", request.ticker(),
                "start_date", request.startDate().toString(),
                "end_date", request.endDate().toString()
        );

        // 2. HTTP POST call to the Python service
        PythonEngineResponse response = restTemplate.postForObject(
                pythonEngineUrl,
                pythonPayload,
                PythonEngineResponse.class
        );

        // 3. Map the returned calculations into our DB Entity format
        TradingStrategy strategy = new TradingStrategy();
        strategy.setPlainEnglishRules(request.prompt());
        strategy.setTicker(request.ticker());
        strategy.setStartDate(request.startDate());
        strategy.setEndDate(request.endDate());

        if (response != null) {
            strategy.setTotalReturn(response.totalReturn());
            strategy.setSharpeRatio(response.sharpeRatio());
            strategy.setMaxDrawdown(response.maxDrawdown());
            strategy.setEquityCurveJson(response.equityCurveJson());
        }

        // 4. Save to PostgreSQL database
        return strategyRepository.save(strategy);
    }
}