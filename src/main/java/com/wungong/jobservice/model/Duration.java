package com.wungong.jobservice.model;

import java.util.Date;

import lombok.Data;

public class Duration {
	
	private final Date startDate;
	private final Date endDate;
	
	public Duration(Date startDate, Date endDate) {
		this.startDate = startDate;
		this.endDate = endDate;
	}

	public Date getStartDate() {
		return startDate;
	}

	public Date getEndDate() {
		return endDate;
	}

}
