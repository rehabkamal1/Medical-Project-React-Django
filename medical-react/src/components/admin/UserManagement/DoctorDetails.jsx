import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Typography,
  Card,
  CardContent,
  Avatar,
  Grid,
  Button,
  Paper,
  Alert,
  CircularProgress,
  Dialog,
  DialogTitle,
  DialogContent,
  TextField,
  DialogActions,
  MenuItem,
  Snackbar,
  Divider,
  InputLabel,
  FormControl,
  Select,
} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import PersonIcon from "@mui/icons-material/Person";

const getAuthToken = () => {
  return localStorage.getItem("access_token");
};

const DoctorDetails = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  // Hardcoded specializations - matching Django backend Doctor model SPECIALIZATION_CHOICES
  const SPECIALIZATION_CHOICES = [
    { id: 1, name: "General" },
    { id: 2, name: "Lungs Specialist" },
    { id: 3, name: "Dentist" },
    { id: 4, name: "Psychiatrist" },
    { id: 5, name: "Covid-19" },
    { id: 6, name: "Surgeon" },
    { id: 7, name: "Cardiologist" },
  ];

  const [doctor, setDoctor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [form, setForm] = useState({
    first_name: "",
    last_name: "",
    username: "",
    email: "",
    phone: "",
    specialization: "",
    bio: "",
    address: "",
  });
  const [errors, setErrors] = useState({});
  const [snackbar, setSnackbar] = useState({
    open: false,
    severity: "success",
    message: "",
  });

  const validateEmail = (email) => {
    if (!email) return true;
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const validatePhone = (phone) => {
    if (!phone) return true;
    return /^[0-9]{10,15}$/.test(phone);
  };

  const validateForm = () => {
    const newErrors = {};
    // Specialization is required
    if (!form.specialization) {
      newErrors.specialization = "Specialization is required";
    }
    // Phone is required
    if (!form.phone) {
      newErrors.phone = "Phone is required";
    } else if (!validatePhone(form.phone)) {
      newErrors.phone = "Invalid phone number (10-15 digits)";
    }
    if (form.email && !validateEmail(form.email))
      newErrors.email = "Invalid email format";
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const fetchDoctorDetails = async () => {
    try {
      setLoading(true);
      setError(null);
      const token = getAuthToken();

      const doctorRes = await fetch(
        `http://127.0.0.1:8000/api/doctor/doctors/${id}/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        },
      );

      if (doctorRes.status === 401) {
        setSnackbar({
          open: true,
          message: "Session expired. Please login again.",
          severity: "error",
        });
        navigate("/login");
        return;
      }

      const doctorData = await doctorRes.json();

      setDoctor(doctorData);
      const firstName = doctorData.user?.first_name || "";
      const lastName = doctorData.user?.last_name || "";
      setForm({
        first_name: firstName,
        last_name: lastName,
        username: doctorData.user?.username || "",
        email: doctorData.user?.email || "",
        phone: doctorData.phone || "",
        specialization: doctorData.specialization || "",
        bio: doctorData.bio || "",
        address: doctorData.address || "",
      });
    } catch (err) {
      setError(err.message || "An error occurred");
      console.error("Error fetching doctor:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDoctorDetails();
  }, [id]);

  const handleOpenEdit = () => {
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    setErrors({});
  };

  const handleSave = async () => {
    if (!validateForm()) return;

    try {
      const token = getAuthToken();
      const url = `http://127.0.0.1:8000/api/doctor/doctors/${id}/`;

      const headers = {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      };

      const requestData = {
        user: {
          username: form.username,
          first_name: form.first_name,
          last_name: form.last_name,
          email: form.email,
        },
        specialization: form.specialization,
        phone: form.phone,
        bio: form.bio,
        address: form.address,
      };

      console.log("Sending request data:", requestData);

      const response = await fetch(url, {
        method: "PUT",
        headers,
        body: JSON.stringify(requestData),
      });

      const responseData = await response.json();
      console.log("Response data:", responseData);

      if (!response.ok) {
        if (response.status === 401) {
          setSnackbar({
            open: true,
            message: "Session expired. Please login again.",
            severity: "error",
          });
          navigate("/admin/login");
          return;
        }
        // Log detailed error info
        console.error("Backend error:", responseData);
        throw new Error(JSON.stringify(responseData));
      }

      fetchDoctorDetails();
      setOpenDialog(false);
      setSnackbar({
        open: true,
        message: "Doctor updated successfully",
        severity: "success",
      });
    } catch (error) {
      console.error("Error details:", error.message);
      setSnackbar({
        open: true,
        message: `Failed to update doctor: ${error.message}`,
        severity: "error",
      });
    }
  };

  const getSpecialtyName = (specialization) => {
    if (!specialization) return "Without specialization";
    const specialty = SPECIALIZATION_CHOICES.find(
      (s) => s.name === specialization,
    );
    return specialty
      ? specialty.name
      : specialization || "Without specialization";
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 4 }}>
        <Alert severity="error" sx={{ mb: 3 }}>
          <Typography variant="h6">Error Loading Doctor Details</Typography>
          <Typography>{error}</Typography>
          <Button
            variant="contained"
            onClick={() => window.location.reload()}
            sx={{ mt: 2 }}
          >
            Try Again
          </Button>
        </Alert>
      </Box>
    );
  }

  if (!doctor) {
    return (
      <Box sx={{ p: 4 }}>
        <Typography variant="h6" sx={{ mt: 4 }}>
          Doctor not found
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ backgroundColor: "#F5F8FF", minHeight: "100vh", p: 4 }}>
      <Paper elevation={3} sx={{ p: 3, borderRadius: "24px" }}>
        <Typography
          variant="h5"
          sx={{ mb: 3, color: "#199A8E", fontWeight: "bold" }}
        >
          Doctor Details
        </Typography>

        <Card sx={{ mb: 3, boxShadow: 3 }}>
          <CardContent>
            <Grid container spacing={3} alignItems="center">
              <Grid item>
                <Avatar
                  src={doctor.image || "/default-avatar.png"}
                  alt={doctor.full_name}
                  sx={{ width: 120, height: 120 }}
                />
              </Grid>
              <Grid item xs>
                <Typography variant="h4" gutterBottom>
                  {doctor.full_name || "No name provided"}
                </Typography>
                <Divider sx={{ my: 2 }} />
                <Typography
                  variant="h6"
                  sx={{
                    mb: 1,
                    display: "flex",
                    alignItems: "center",
                    gap: 1,
                  }}
                >
                  <PersonIcon /> Personal Information
                </Typography>
                <Box sx={{ mb: 1 }}>
                  <Typography variant="body1">
                    <strong>Specialty:</strong>{" "}
                    {getSpecialtyName(doctor.specialization)}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Email:</strong> {doctor.user?.email || "N/A"}
                  </Typography>
                  <Typography variant="body1">
                    <strong>Phone:</strong> {doctor.phone || "Not Set"}
                  </Typography>
                  {doctor.address && (
                    <Typography variant="body1">
                      <strong>Address:</strong> {doctor.address}
                    </Typography>
                  )}
                </Box>
                {doctor.bio && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="subtitle1" gutterBottom>
                      <strong>Bio:</strong>
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {doctor.bio}
                    </Typography>
                  </Box>
                )}
              </Grid>
            </Grid>
          </CardContent>
        </Card>

        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<EditIcon />}
            onClick={handleOpenEdit}
          >
            Edit Doctor
          </Button>
          <Button variant="outlined" onClick={() => navigate("/admin/doctors")}>
            Back to Doctors List
          </Button>
        </Box>
      </Paper>

      <Dialog
        open={openDialog}
        onClose={handleCloseDialog}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Edit Doctor</DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", gap: 2 }}>
            <TextField
              label="First Name"
              name="first_name"
              value={form.first_name}
              onChange={(e) => setForm({ ...form, first_name: e.target.value })}
              error={!!errors.first_name}
              helperText={errors.first_name}
              fullWidth
              margin="normal"
            />
            <TextField
              label="Last Name"
              name="last_name"
              value={form.last_name}
              onChange={(e) => setForm({ ...form, last_name: e.target.value })}
              error={!!errors.last_name}
              helperText={errors.last_name}
              fullWidth
              margin="normal"
            />
          </Box>
          <TextField
            label="Username"
            name="username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            fullWidth
            margin="normal"
            disabled
          />
          <TextField
            label="Email"
            name="email"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
            error={!!errors.email}
            helperText={errors.email}
            fullWidth
            margin="normal"
          />
          <TextField
            label="Phone *"
            name="phone"
            value={form.phone}
            onChange={(e) => setForm({ ...form, phone: e.target.value })}
            error={!!errors.phone}
            helperText={errors.phone}
            fullWidth
            margin="normal"
          />
          <FormControl
            fullWidth
            margin="normal"
            error={!!errors.specialization}
          >
            <InputLabel>Specialty *</InputLabel>
            <Select
              value={form.specialization}
              onChange={(e) =>
                setForm({ ...form, specialization: e.target.value })
              }
              label="Specialty *"
            >
              <MenuItem value="">Select a specialty</MenuItem>
              {SPECIALIZATION_CHOICES.map((spec) => (
                <MenuItem key={spec.id} value={spec.name}>
                  {spec.name}
                </MenuItem>
              ))}
            </Select>
            {errors.specialization && (
              <Box sx={{ color: "#d32f2f", fontSize: "0.75rem", mt: 0.5 }}>
                {errors.specialization}
              </Box>
            )}
          </FormControl>
          <TextField
            label="Bio"
            name="bio"
            value={form.bio}
            onChange={(e) => setForm({ ...form, bio: e.target.value })}
            fullWidth
            multiline
            rows={3}
            margin="normal"
          />
          <TextField
            label="Address"
            name="address"
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
            fullWidth
            margin="normal"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button variant="contained" onClick={handleSave}>
            Update
          </Button>
        </DialogActions>
      </Dialog>

      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert severity={snackbar.severity}>{snackbar.message}</Alert>
      </Snackbar>
    </Box>
  );
};

export default DoctorDetails;
