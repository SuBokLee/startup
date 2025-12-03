// ... existing code ...
      const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      
      // 디버깅: 실제 요청 URL 확인
      console.log("API_URL:", API_URL);
      console.log("Request URL:", `${API_URL}/chat`);
      
      const response = await fetch(`${API_URL}/chat`, {
// ... existing code ...
