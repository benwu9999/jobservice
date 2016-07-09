package com.wungong.jobservice.model;

import lombok.Data;

@Data
public class Duty {
	
	private final String description;

	public Duty(String description) {
		this.description = description;
	}

	public String getDescription() {
		return description;
	}

}
