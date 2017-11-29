package com.tms.beans;

public class MyConstants {

	public static String ACTION_ADD = "add";
	public static String ACTION_UPDATE = "update";
	public static String ACTION_DELETE = "delete";
	
	public static String MYSQL_DATE_TIME_FORMATER = "yyyy-MM-dd HH:mm:ss";

	public static String SUCCESS = "Success";
	
	public static String SESSION_EXPIRED = "Session Expired. Please login again";
	
    public static String USER_NAME_BLANK = "Please enter user name.";

    public static String MISMATCH_SECURITY_CODE = "Mismatch security code.";

    public static String SECURITY_CODE_BLANK = "Please enter security code.";

    public static String PASSWORD_BLANK = "Please enter password.";
    

	public static String INVALID_USERNAME_PASSWORD = "Invalid Username Or Password";
	
	public static String DONT_HAVE_PERMISSION = "You dont have permission.";

	// Different types of status
	public static String STATUS_INSTOCK = "InStock";
	public static String STATUS_INSTALLED = "Installed";
	public static String STATUS_SCRAPED = "Scraped";

	public static String STATUS_ERROR = "Incorrent status. Status should be "+STATUS_INSTOCK+", "+STATUS_INSTALLED+" or "+STATUS_SCRAPED;
	
	// Tire inspection
	public static String SELECT_TIRE = "Please select a tire.";
	
	public static String LOCATION_REQUIRED = "Position required";
	
	public static String KMSREADING_REQUIRED = "KMS Reading required";
	
	public static String TREAD_DEPTH_LOCATION1_REQUIRED = "Tread Depth Location1 required";
	public static String TREAD_DEPTH_LOCATION2_REQUIRED = "Tread Depth Location2 required";
	public static String TREAD_DEPTH_LOCATION3_REQUIRED = "Tread Depth Location3 required";
	
	public static String TIRE_PRESSURE_REQUIRED = "Tire pressure required";
	
	// Add, Update and Deletion of vehicle
	public static String VEHICLE_NAME_REQUIRED = "vehicle name required.";
	public static String VEHICLE_ID_REQUIRED = "vehicle Id required.";

	public static String VEHICLE_EXISTS = "vehicle already exists.";
	public static String VEHICLEID_NOT_EXISTS = "vehicleId not exists.";
	public static String VEHICLE_NOT_EXISTS = "vehicle not exists.";

	public static String VEHICLE_ADDED_SUCCESSFULL = "Vehicle added successfully.";
	public static String VEHICLE_UPDATED_SUCCESSFULL = "Vehicle updated successfully.";
	public static String VEHICLE_DELETED_SUCCESSFULL = "Vehicle deleted successfully.";

	public static String VEHICLE_ADDING_FAILED = "Unable to add vehicle details. Please contact Admin";
	public static String VEHICLE_UPDATING_FAILED = "Unable to update vehicle details. Please contact Admin";
	public static String VEHICLE_DELETING_FAILED = "Unable to delete vehicle details. Please contact Admin";
	
	public static String ATLEAST_ONE_VEHICLE_NEEDED = "Please select atleast one Vehicle.";
	
	public static String ATLEAST_ONE_USER_NEEDED = "Please select atleast one User.";
	
	public static String CHECK_YOUR_REQUEST = "Please check your request.";

	public static String VEHICLE_MAPPED_USER_SUCCESS = "Vehicles assigned successfully.";
	
	public static String VEHICLE_MAPPED_USER_FAILED = "Vehicle is not assigned to User. Please try again later.";
	
	public static String SEARCH_WORD_REQUIRED = "Please enter some search word";
	
	public static String EXISTS = " already exists";
	
	public static String NOT_EXISTS = " not exists";

	// Add, Update and Deletion of RFID
	public static String RFIDUID_REQUIRED = "RFID UID is required";
	public static String RFID_REQUIRED = "RFID is required";

	public static String RFID_NOT_EXISTS = "RFID not exists.";
	public static String RFIDUID__EXISTS = " already exists.";

	public static String RFID_ADDED_SUCCESSFULLY = "RFID added successfully";
	public static String RFID_UPDATED_SUCCESSFULL = "RFID updated successfully.";
	public static String RFID_DELETED_SUCCESSFULL = "RFID deleted successfully.";

	public static String RFID_ADDING_FAILED = "Unable to add RFID. Please contact Admin.";
	public static String RFID_UPDATING_FAILED = "Unable to update RFID details. Please contact Admin.";
	public static String RFID_DELETING_FAILED = "Unable to delete RFID details. Please contact Admin.";

	// Add, Update and Delete of Bluetooth controller
	public static String BControllerUID_REQUIRED = "Bluetooth Controller UID is required";
	public static String BControllerID_REQUIRED = "BControllerId is required";

	public static String BControllerId_NOT_EXISTS = "BControllerId not exists.";
	public static String BControllerUID__EXISTS = " already exists.";

	public static String BController_ADDED_SUCCESSFULLY = "Bluetooth Controller added successfully";
	public static String BController_UPDATED_SUCCESSFULL = "Bluetooth Controller updated successfully.";
	public static String BController_DELETED_SUCCESSFULL = "Bluetooth Controller deleted successfully.";

	public static String BController_ADDING_FAILED = "Unable to add Bluetooth Controller. Please contact Admin.";
	public static String BController_UPDATING_FAILED = "Unable to update Bluetooth Controller details. Please contact Admin.";
	public static String BController_DELETING_FAILED = "Unable to delete Bluetooth Controller details. Please contact Admin.";

	// Add, Update and Delete of Sensor
	public static String SENSORUID_REQUIRED = "Sensor UID is required";
	public static String SENSORID_REQUIRED = "sensorId is required";

	public static String SENSORUID__EXISTS = "Sensor UID already exists.";
	public static String SENSORID_NOT_EXISTS = "sensorId not exists.";
	
	public static String SENSOR_NOT_EXISTS = "Sensor is not exists in DB.";
	
	public static String SENSOR_ASSIGNED_ALREADY = "Sensor is already assigned to other tire";

	public static String SENSOR_ADDED_SUCCESSFULLY = "Sensor added successfully";
	public static String SENSOR_UPDATED_SUCCESSFULL = "Sensor updated successfully.";
	public static String SENSOR_DELETED_SUCCESSFULL = "Sensor deleted successfully.";

	public static String SENSOR_ADDING_FAILED = "Unable to add Sensor. Please contact Admin.";
	public static String SENSOR_DELETING_FAILED = "Unable to delete Sensor details. Please contact Admin.";
	public static String SENSOR_UPDATING_FAILED = "Unable to update Sensor details. Please contact Admin.";

	// Add, Update and Delete of Tire
	public static String TIRENUMBER_REQUIRED = "Tire Number is required";
	public static String TIRE_TYPE_REQUIRED = "Tire type is required";
	public static String TIREMAKE_REQUIRED = "Tire Make is required";
	public static String DEPOT_REQUIRED = "Depot is required";
	public static String TIREID_REQUIRED = "tireId is required";
	public static String TIREPOSITION_REQUIRED = "Tire position is required";
	public static String THREAD_DEPTH_REQUIRED = "Thread Depth is required";
	
	public static String ASSIGN_SENSOR= "Please assign a sensor to Tire first then assign tire to vehicle.";

	public static String TIRENUMBER__EXISTS = "Tire Number already exists.";
	public static String TIREID_NOT_EXISTS = "TireId not exists.";
	public static String TIRE_NOT_EXISTS = "Tire not exists.";

	public static String TIRE_ADDED_SUCCESSFULLY = "Tire added successfully";
	public static String TIRE_ASSIGNED_SUCCESSFULLY = "Tire assigned successfully";
	public static String TIRE_UPDATED_SUCCESSFULL = "Tire updated successfully.";
	public static String TIRE_DELETED_SUCCESSFULL = "Tire deleted successfully.";
	
	public static String TIRE_DEALLOCATED_SUCCESS = "Tire deallocated successfully";
	
	public static String TIRE_DEALLOCATED_FAILED = "Unable to deallocate the tire. Please contact admin.";
	
	public static String TIRE_NOT_ASSIGNED_TO_THIS_VEHICLE = "Tire is not assigned to vehicle";

	public static String TIRE_ADDING_FAILED = "Unable to add Tire details. Please contact Admin.";
	public static String TIRE_DELETING_FAILED = "Unable to delete Tire details. Please contact Admin.";
	public static String TIRE_UPDATING_FAILED = "Unable to update Tire details. Please contact Admin.";
	
	// TMS Organization
	public static String ORG_NAME_REQUIRED = "Organization Name is required";
	
	public static String ORG_ID_REQUIRED = "Organization Id is required";
	
	public static String ORG_NAME_EXISTS = "Organization Name already exists";
	
	public static String ORG_ADDING_SUCCESS = "Organization add successfully";
	
	public static String ORG_ADDING_FAILED = "Unable to add Organization";
	
	// TMS Depot
	public static String DEPOT_NAME_REQUIRED = "Depot Name is required";
	
	public static String DEPOT_NAME_EXISTS = "Depot Name already exists";
	
	public static String DEPOT_NOT_EXISTS = "Depot not exists";
	
	public static String DEPOT_ADDING_SUCCESS = "Depot added successfully";
	
	public static String DEPOT_ADDING_FAILED = "Unable to add Depot";
	
	//Tire Inspection
	public static String TIRE_INSPECTION_ADDING_SUCCESS = "Tire Inspection details are added successfully";
	
	public static String TIRE_INSPECTION_ADDING_FAILED = "Unable to save Inspection details. Please try again later.";
	
	public static String TIRE_INSPECTION_UPDATE_SUCCESS = "Tire Inspection details are updated successfully";
	
	public static String TIRE_INSPECTION_UPDATE_FAILED = "Unable to update Inspection details. Please try again later.";
	
	public static String INVALID_INSPECTION_ID = "Invalid inspection Id";
	
	public static String INSPECTION_NOT_FOUND = "Inspection details are found with id. Please try again later.";
	
	//Tire Service
	public static String TIRE_SERVICE_ADDING_SUCCESS = "Tire Service details are added successfully";
	
	public static String TIRE_SERVICE_ADDING_FAILED = "Unable to save Service details. Please try again later.";
	
	public static String TIRE_SERVICE_UPDATE_SUCCESS = "Tire Service details are updated successfully";
	
	public static String TIRE_SERVICE_UPDATE_FAILED = "Unable to update service details. Please try again later.";
	
	public static String INVALID_SERVICE_ID = "Invalid service Id";
	
	public static String SERVICE_NOT_FOUND = "Service details are not found with id. Please try again later.";
	
	public static String BUS_NO_REQUIRED = "Bus No is required";
	
	public static String FITTED_DATE_REQUIRED = "Fitted Date is required";
	
	public static String FITTED_KMS_REQUIRED = "Fitment KM is required";
	
	public static String TIRE_REMOVAL_DATE_REQUIRED = "Removal Date is required";
	
	public static String REMOVAL_KMS_REQUIRED = "Removal KM is required";
	
	public static String REASON_REQUIRED = "Reason for Removal is required";
	
	public static String ACTION_REQUIRED = "Action Taken is required";
	
	public static String TIRE_CONDITION_REQUIRED = "Tyre Condition is required";
	
	public static String TIRE_SCRAPPED_PARTY_REQUIRED = "Tyre Scrapped to Party is required";
	
	public static String SERVICE_EXISTS_ON_FITTED_DATE = "Service already exists on this fitted date";
	
	public static String SERVICE_EXISTS_ON_REMOVAL_DATE = "Service already exists on this removal date";
	
	public static String SERVICE_EXISTS_ON_THESE_DATES = "Service already exists on these dates";
	
	public static String FITMENT_KM_GREATERTHAN_REMOVAL_KM = "Removal KM should be greater than the fitment KM";
	
	public static String FITMENT_DATE_GREATERTHAN_REMOVAL_DATE = "Removal date should be greater than the fitment date";
	
	public static String FITMENT_DETAILS_NOT_EXISTS = "Tyre fitment details are not exists. Please contact admin and share this data.";

	public static String UNABLE_TO_PROCESS_REQUEST = "Unable to process your request. Please try again.";

}
