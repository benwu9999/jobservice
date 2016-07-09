package com.wungong.jobservice.model;

import lombok.Data;

public class Benefit {
	
	private final String description;

	public Benefit(String description) {
		this.description = description;
	}

	public String getDescription() {
		return description;
	}

}
