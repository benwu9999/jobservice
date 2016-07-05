package com.wungong.jobservice.controller;

import javax.ws.rs.core.Response;

import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.wungong.jobservice.request.JobRequest;
import com.wungong.jobservice.response.JobResponse;
import com.wungong.jobservice.response.JobResponseImpl;

@RestController
@RequestMapping("/job")
public class JobserviceController {
	
	@RequestMapping(method = RequestMethod.POST, consumes="application/json", produces="application/json")
    public JobResponse createJob(JobRequest request) {
		return new JobResponseImpl(Response.Status.CREATED);
    }
	
	@RequestMapping(method = RequestMethod.DELETE, consumes="application/json", produces="application/json")
    public JobResponse deleteJob(JobRequest request) {
		return new JobResponseImpl(Response.Status.OK);
    }
	
	@RequestMapping(method = RequestMethod.PUT, consumes="application/json", produces="application/json")
    public JobResponse updateJob(JobRequest request) {
		return new JobResponseImpl(Response.Status.OK);
    }
	
	@RequestMapping(method = RequestMethod.GET, params="id", produces="application/json")
    public JobResponse getJob(@RequestParam("id") Long id) {
		return new JobResponseImpl(Response.Status.OK);
    }
}
