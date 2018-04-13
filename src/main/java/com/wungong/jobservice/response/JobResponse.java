package com.wungong.jobservice.response;

import com.wungong.jobservice.model.Job;

public interface JobResponse {

	Integer getStatus();
	
	Job getJob();
	
}
