import React, { useState } from "react";
import axios from "axios";
import Dialog from "./Dialog";

type InvoiceFormProps = {
  onClose: () => void,
}

const InvoiceForm: React.FC<InvoiceFormProps> = ({ onClose }) => {
  const [formData, setFormData] = useState({
    productName: "",
    hsCode: "",
    totalPrice: "",
    description: "",
  });

  const [analysis, setAnalysis] = useState<boolean>(false)


  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value }: { name: any, value: any } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log("Form Data Submitted:", formData);
    onClose();
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return

    const formData = new FormData()
    formData.append('file', file);
    try {
      const res = await axios.post("http://127.0.0.1:5000/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const temp = JSON.parse(res.data.hs_code)
      console.log(temp)
      setFormData({
        ...temp
      })
      setTimeout(() => {
        setAnalysis(true);

      },1000)
    } catch (error) {
      console.error("Error uploading file:", error);
      alert("Failed to upload file");
    }
  }

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      {!analysis?
      <div className="mx-auto bg-white p-8 rounded-lg shadow-lg">
        <div className="flex items-center justify-center min-h-[10vh]">
          <div className="flex items-center space-x-4">
            <h1 className="text-2xl font-bold text-blue-600">
              Invoice Form
            </h1>
            <input
              type="file"
              className="block text-sm text-gray-500 
                 file:mr-4 file:py-2 file:px-4
                 file:rounded-lg file:border-0
                 file:text-sm file:font-semibold
                 file:bg-blue-50 file:text-blue-700
                 hover:file:bg-blue-100"
              onChange={handleFileUpload}
            />
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">

          {/* Product Details */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Product Name
              </label>
              <input
                type="text"
                name="productName"
                value={formData.productName}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                HS Code
              </label>
              <input
                type="text"
                name="hsCode"
                value={formData.hsCode}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Price
              </label>
              <input
                type="text"
                name="totalPrice"
                value={formData.totalPrice}
                onChange={handleChange}
                className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                required
              />
            </div>
          </div>

          {/* Total Price */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              description
            </label>
            <input
              type="text"
              name="description"
              value={formData.description}
              onChange={handleChange}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              required
            />
          </div>

          {/* Submit Button */}
          <div className="flex justify-center bg-blue">
            <button
              type="submit"
              className="px-6 py-2 bg-blue font-semibold rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Submit
            </button>
          </div>
        </form>
      </div>:
      <Dialog isOpen={analysis} onClose={() => {
        setAnalysis(false)
      }} hs_code={Number(formData.hsCode)} description={formData.description} name={formData.productName} price={Number(formData.totalPrice) || 50000}/>
      }
    </div>
  );
};

export default InvoiceForm;