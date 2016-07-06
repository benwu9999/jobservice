package com.wungong.jobservice.model;

import lombok.Data;

@Data
public class Compensation {
	
	private final Integer amount;
	
	private final TimePeriod timePeriod;

}
