package com.wungong.jobservice.model;

import java.util.Date;

import lombok.Data;

@Data
public class TimePeriod {
	
	private final Date startDate;
	private final Date endDate;

}
