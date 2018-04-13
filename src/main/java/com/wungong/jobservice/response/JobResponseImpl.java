package com.wungong.jobservice.response;

import javax.ws.rs.core.Response;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.wungong.jobservice.model.Job;

public class JobResponseImpl implements JobResponse {
	
	@JsonProperty
	private Response.Status status;
	
	@JsonProperty
	private String body;
	
	@JsonProperty
	private Job job;

	public JobResponseImpl(Response.Status status) {
		this.status = status;
	}

	@Override
	public Integer getStatus() {
		return status.getStatusCode();
	}

	@Override
	public Job getJob() {
		return job;
	}

}
