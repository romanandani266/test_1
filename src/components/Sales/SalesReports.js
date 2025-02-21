import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchSalesReport } from '../../redux/slices/salesSlice';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const SalesReports = () => {
  const dispatch = useDispatch();
  const salesData = useSelector((state) => state.sales.data);

  useEffect(() => {
    dispatch(fetchSalesReport());
  }, [dispatch]);

  return (
    <LineChart width={600} height={300} data={salesData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="sales" stroke="#8884d8" />
    </LineChart>
  );
};

export default SalesReports;