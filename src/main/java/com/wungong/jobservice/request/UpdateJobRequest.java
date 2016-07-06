package com.wungong.jobservice.request;

import lombok.Data;

@Data
public class UpdateJobRequest extends CreateJobRequest{
	
	final private String jobId;

}
