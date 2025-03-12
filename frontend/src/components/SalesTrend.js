import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../api';

const SalesTrend = () => {
  const { id } = useParams();
  const [salesTrend, setSalesTrend] = useState([]);

  useEffect(() => {
    const fetchSalesTrend = async () => {
      try {
        const data = await api.getSalesTrend(id);
        setSalesTrend(data);
      } catch (error) {
        console.error('Error fetching sales trend:', error);
      }
    };
    fetchSalesTrend();
  }, [id]);

  return (
    <div>
      <h2>Sales Trend</h2>
      <ul>
        {salesTrend.map((trend, index) => (
          <li key={index}>{trend}</li>
        ))}
      </ul>
    </div>
  );
};

export default SalesTrend;
