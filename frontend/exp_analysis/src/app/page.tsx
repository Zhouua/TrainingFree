"use client";

import { useEffect, useState, Suspense, useRef } from "react";
import {
  Card,
  Table,
  Button,
  Input,
  Select,
  Statistic,
  Row,
  Col,
  Pagination,
  Dropdown,
  Menu,
  ConfigProvider,
  theme,
  Switch,
  Space
} from "antd";
import { useRouter, useSearchParams } from "next/navigation";
import { FilterOutlined, FilterFilled, BulbOutlined, BulbFilled } from "@ant-design/icons";

type Evaluation = {
  id: number;
  trace_id: string;
  exp_id: string;
  source: string;
  raw_question: string;
  level: number | null;
  augmented_question: string | null;
  correct_answer: string | null;
  file_name: string | null;
  stage: string;
  response: string | null;
  time_cost: number | null;
  trajectory: string | null;
  extracted_final_answer: string | null;
  judged_response: string | null;
  reasoning: string | null;
  correct: boolean | null;
  confidence: number | null;
  dataset_index: number; // 确保有这个字段
};

type FilterState = {
  keyword: string;
  tools: string;
};

function HomePageContentWrapper() {
  return (
      <Suspense fallback={<div>Loading...</div>}>
        <HomePageContent />
      </Suspense>
  );
}

function HomePageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  // 使用Ant Design的主题状态
  const [isDarkMode, setIsDarkMode] = useState(false);

  const [expIds, setExpIds] = useState<string[]>([]);
  const [selectedExpId, setSelectedExpId] = useState<string | null>(null);
  const [allEvaluations, setAllEvaluations] = useState<Evaluation[]>([]);
  const [stats, setStats] = useState<{ [key: string]: number }>({});
  const [isLoading, setIsLoading] = useState(false);

  const [filter, setFilter] = useState<FilterState>({
    keyword: "",
    tools: ""
  });

  const [appliedFilter, setAppliedFilter] = useState<FilterState>({
    keyword: "",
    tools: ""
  });

  const [correctFilter, setCorrectFilter] = useState<string>("all");
  const [appliedCorrectFilter, setAppliedCorrectFilter] = useState<string>("all");

  const [traceId, setTraceId] = useState("");
  const [appliedTraceId, setAppliedTraceId] = useState("");

  const urlPage = searchParams.get('page');
  const urlPageSize = searchParams.get('pageSize');

  const [currentPage, setCurrentPage] = useState(
      urlPage ? Number(urlPage) : 1
  );
  const [pageSize, setPageSize] = useState(
      urlPageSize ? Number(urlPageSize) : 20
  );
  const [totalItems, setTotalItems] = useState(0);

  const initializedRef = useRef(false);

  useEffect(() => {
    if (initializedRef.current) return;
    initializedRef.current = true;

    const savedTheme = localStorage.getItem("theme");
    const initialDarkMode = savedTheme === "dark";
    setIsDarkMode(initialDarkMode);

    document.body.className = initialDarkMode ? "dark-mode" : "light-mode";

    fetch("/api/exp_ids")
        .then((res) => res.json())
        .then((data) => {
          setExpIds(data);
          const urlExpId = searchParams.get("exp_id");
          const urlCorrect = searchParams.get("correct") || "all";
          const urlKeyword = searchParams.get("keyword") || "";
          const urlTools = searchParams.get("tools") || "";
          const urlTraceId = searchParams.get("trace_id") || "";

          setFilter({
            keyword: urlKeyword,
            tools: urlTools
          });

          setAppliedFilter({
            keyword: urlKeyword,
            tools: urlTools
          });

          setCorrectFilter(urlCorrect);
          setAppliedCorrectFilter(urlCorrect);
          setTraceId(urlTraceId);
          setAppliedTraceId(urlTraceId);

          if (urlExpId && (data.includes(urlExpId) || urlExpId === "all")) {
            setSelectedExpId(urlExpId);
          } else if (data.length > 0) {
            setSelectedExpId(data[0]);
          } else {
            // 如果没有可用的实验ID，也要允许选择all
            setSelectedExpId("all");
          }
        });
  }, [searchParams]);

  // 保存主题设置并更新body样式
  useEffect(() => {
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");
    document.body.className = isDarkMode ? "dark-mode" : "light-mode";
  }, [isDarkMode]);

  useEffect(() => {
    if (selectedExpId || selectedExpId === "all") {
      setIsLoading(true);

      const newSearchParams = new URLSearchParams();
      if (selectedExpId !== "all") {
        newSearchParams.set("exp_id", selectedExpId);
      }
      newSearchParams.set("page", currentPage.toString());
      newSearchParams.set("pageSize", pageSize.toString());
      newSearchParams.set("order", "dataset_index");

      if (appliedFilter.keyword) newSearchParams.set("keyword", appliedFilter.keyword);
      if (appliedFilter.tools) newSearchParams.set("tools", appliedFilter.tools);
      if (appliedTraceId) newSearchParams.set("trace_id", appliedTraceId);
      if (appliedCorrectFilter !== "all") newSearchParams.set("correct", appliedCorrectFilter);

      const urlParams = new URLSearchParams(newSearchParams);
      if (urlParams.toString() !== searchParams.toString()) {
        router.replace(`/?${urlParams.toString()}`, { scroll: false });
      }

      if (selectedExpId === "all" && !appliedTraceId) {
        setAllEvaluations([]);
        setTotalItems(0);
        setIsLoading(false);
        return;
      }

      const apiPath = selectedExpId === "all"
          ? `/api/evaluations/all?${newSearchParams.toString()}`
          : `/api/evaluations/${selectedExpId}?${newSearchParams.toString()}`;

      fetch(apiPath)
          .then((res) => res.json())
          .then((data) => {
            setAllEvaluations(data.data || []);
            setTotalItems(data.totalCount || 0);
            setIsLoading(false);
          })
          .catch((error) => {
            console.error("Error fetching evaluations:", error);
            setIsLoading(false);
            setAllEvaluations([]);
            setTotalItems(0);
          });

      // 统计信息请求（不需要分页参数）
      const statsParams = new URLSearchParams();
      if (selectedExpId !== "all") statsParams.set("exp_id", selectedExpId);
      if (appliedFilter.keyword) statsParams.set("keyword", appliedFilter.keyword);
      if (appliedFilter.tools) statsParams.set("tools", appliedFilter.tools);
      if (appliedTraceId) statsParams.set("trace_id", appliedTraceId);
      if (appliedCorrectFilter !== "all") statsParams.set("correct", appliedCorrectFilter);

      const statsPath = selectedExpId === "all"
          ? `/api/evaluations/all/stats?${statsParams.toString()}`
          : `/api/evaluations/${selectedExpId}/stats?${statsParams.toString()}`;

      fetch(statsPath)
          .then((res) => res.json())
          .then(setStats);
    }
  }, [selectedExpId, appliedFilter, appliedCorrectFilter, appliedTraceId, searchParams, router, currentPage, pageSize]);

  const handleFilterChange = (field: keyof FilterState, value: string) => {
    setFilter(prev => ({ ...prev, [field]: value }));
  };

  const handleTraceIdChange = (value: string) => {
    setTraceId(value);
  };

  const handleQuery = () => {
    setAppliedFilter(filter);
    setAppliedCorrectFilter(correctFilter);
    setAppliedTraceId(traceId);
    setCurrentPage(1);
  };

  const handleClearFilters = () => {
    setFilter({ keyword: "", tools: "" });
    setCorrectFilter("all");
    setAppliedFilter({ keyword: "", tools: "" });
    setAppliedCorrectFilter("all");
    setTraceId("");
    setAppliedTraceId("");
    setCurrentPage(1);
  };

  const handleRowClick = (evaluationId: number) => {
    const currentSearchParams = new URLSearchParams();
    if (selectedExpId && selectedExpId !== "all") currentSearchParams.set("exp_id", selectedExpId);
    currentSearchParams.set("correct", appliedCorrectFilter);
    if (appliedFilter.keyword) currentSearchParams.set("keyword", appliedFilter.keyword);
    if (appliedFilter.tools) currentSearchParams.set("tools", appliedFilter.tools);
    if (appliedTraceId) currentSearchParams.set("trace_id", appliedTraceId);

    currentSearchParams.set("page", currentPage.toString());
    currentSearchParams.set("pageSize", pageSize.toString());

    router.push(`/evaluations/${evaluationId}?${currentSearchParams.toString()}`);
  };

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  };

  const correctFilterMenu = (
      <Menu
          selectedKeys={[appliedCorrectFilter]}
          onClick={({ key }) => {
            setCorrectFilter(key);
            setAppliedCorrectFilter(key);
            setCurrentPage(1);
          }}
      >
        <Menu.Item key="all">All</Menu.Item>
        <Menu.Item key="true">True</Menu.Item>
        <Menu.Item key="false">False</Menu.Item>
      </Menu>
  );

  const FilterIcon = appliedCorrectFilter !== "all" ? FilterFilled : FilterOutlined;

  const columns = [
    {
      title: "Trace ID",
      dataIndex: "trace_id",
      key: "trace_id",
      width: 120,
      render: (text: string) => (
          <span className={isDarkMode ? "text-blue-300" : "text-blue-500"}>
          {text}
        </span>
      )
    },
    {
      title: "Dataset Index",
      dataIndex: "dataset_index",
      key: "dataset_index",
      width: 100,
      sorter: true
    },
    {
      title: "Source",
      dataIndex: "source",
      key: "source",
      width: 100
    },
    {
      title: "Question",
      dataIndex: "raw_question",
      key: "raw_question",
      width: 200,
      ellipsis: true
    },
    {
      title: "Level",
      dataIndex: "level",
      key: "level",
      width: 80
    },
    {
      title: "Correct Answer",
      dataIndex: "correct_answer",
      key: "correct_answer",
      width: 150,
      ellipsis: true
    },
    {
      title: "Stage",
      dataIndex: "stage",
      key: "stage",
      width: 80
    },
    {
      title: "Response",
      dataIndex: "response",
      key: "response",
      width: 200,
      ellipsis: true
    },
    {
      title: (
          <div className="flex items-center">
            <span>Correct</span>
            <Dropdown
                overlay={correctFilterMenu}
                trigger={['click']}
                open={undefined}
            >
              <FilterIcon
                  className={`ml-2 ${appliedCorrectFilter !== "all" ? (isDarkMode ? "text-blue-300" : "text-blue-500") : "text-gray-400"}`}
              />
            </Dropdown>
          </div>
      ),
      dataIndex: "correct",
      key: "correct",
      width: 100,
      render: (correct: boolean | null) => (
          <span className={`font-medium ${
              correct === true ? (isDarkMode ? "text-green-400" : "text-green-600") :
                  correct === false ? (isDarkMode ? "text-red-400" : "text-red-500") :
                      (isDarkMode ? "text-gray-400" : "text-gray-500")
          }`}>
      {correct === true ? "True" :
          correct === false ? "False" : "N/A"}
    </span>
      )
    },
    {
      title: "Confidence",
      dataIndex: "confidence",
      key: "confidence",
      width: 120,
      render: (value: number | null) => (
          <span className={value ? (isDarkMode ? "text-purple-400" : "text-purple-600") : (isDarkMode ? "text-gray-400" : "text-gray-500")}>
          {value ?? "N/A"}
        </span>
      )
    }
  ];

  return (
      <ConfigProvider
          theme={{
            algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
            token: {
              colorBgContainer: isDarkMode ? "#3c3d32" : "#ffffff",
              colorText: isDarkMode ? "#f8f8f2" : "#333333",
              colorBorder: isDarkMode ? "#49483e" : "#d9d9d9",
            },
            components: {
              Card: {
                headerBg: isDarkMode ? "#3c3d32" : "#fafafa",
                colorTextHeading: isDarkMode ? "#f8f8f2" : "#333333",
              },
              Table: {
                headerBg: isDarkMode ? "#3c3d32" : "#fafafa",
                headerColor: isDarkMode ? "#f8f8f2" : "#333333",
                rowHoverBg: isDarkMode ? "rgba(60, 61, 50, 0.6)" : "#f5f5f5",
              },
              Input: {
                colorBgContainer: isDarkMode ? "#272822" : "#ffffff",
                colorText: isDarkMode ? "#f8f8f2" : "#333333",
                colorBorder: isDarkMode ? "#49483e" : "#d9d9d9",
              },
              Select: {
                colorBgContainer: isDarkMode ? "#272822" : "#ffffff",
                colorText: isDarkMode ? "#f8f8f2" : "#333333",
                colorBorder: isDarkMode ? "#49483e" : "#d9d9d9",
              },
              Button: {
                colorBgContainer: isDarkMode ? "#3c3d32" : "#f0f0f0",
                colorText: isDarkMode ? "#f8f8f2" : "#333333",
              }
            }
          }}
      >
        <div className={`max-w-screen-2xl mx-auto p-4 min-h-screen ${isDarkMode ? "bg-[#272822] text-[#f8f8f2]" : "bg-white text-gray-800"}`}>
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold">LLM Agent Experiments</h1>
            <div className="flex items-center space-x-4">
              {/* 新增Trace ID输入框 */}
              <Input
                  placeholder="Trace ID"
                  value={traceId}
                  onChange={e => handleTraceIdChange(e.target.value)}
                  style={{ width: 320, marginRight: 20}}
              />

              <Select
                  style={{ width: 280 }}
                  onChange={(value) => {
                    setSelectedExpId(value);
                    setCurrentPage(1);
                  }}
                  value={selectedExpId}
                  placeholder="Select an experiment"
                  options={[
                    { label: "All Experiments", value: "all" },
                    ...expIds.map(id => ({ label: id, value: id }))
                  ]}
                  showSearch
                  allowClear
              />

              <Space size={8} className="ml-4">
                <Switch
                    checkedChildren={<BulbFilled />}
                    unCheckedChildren={<BulbOutlined />}
                    checked={isDarkMode}
                    onChange={setIsDarkMode}
                />
                <span>{isDarkMode ? "Dark" : "Light"}</span>
              </Space>
            </div>
          </div>
          {selectedExpId === "all" && !appliedTraceId && allEvaluations.length === 0 && (
              <div className={`p-6 mb-6 rounded-md ${isDarkMode ? "bg-[#49483e] text-red-300" : "bg-red-50 text-red-700"}`}>
                <p className="font-medium">⚠️提示：</p>
                <p className="mt-2">
                  当选择 All Experiments 且未输入Trace ID时，系统不会查询全部数据（避免性能问题）。
                  请输入Trace ID或者选择特定实验ID进行查询。
                </p>
              </div>
          )}
          {selectedExpId && (
              <>
                <Row gutter={16} className="mb-6">
                  <Col span={8}>
                    <Card
                        bordered={false}
                        className={isDarkMode ? "bg-[#3c3d32] border border-[#49483e]" : "bg-gray-50"}
                    >
                      <Statistic
                          title="Init"
                          value={stats.init || 0}
                          valueStyle={{ color: isDarkMode ? '#a6e22e' : '#3f8600' }}
                      />
                    </Card>
                  </Col>
                  <Col span={8}>
                    <Card
                        bordered={false}
                        className={isDarkMode ? "bg-[#3c3d32] border border-[#49483e]" : "bg-gray-50"}
                    >
                      <Statistic
                          title="Rollout"
                          value={stats.rollout || 0}
                          valueStyle={{ color: isDarkMode ? '#66d9ef' : '#1890ff' }}
                      />
                    </Card>
                  </Col>
                  <Col span={8}>
                    <Card
                        bordered={false}
                        className={isDarkMode ? "bg-[#3c3d32] border border-[#49483e]" : "bg-gray-50"}
                    >
                      <Statistic
                          title="Judged"
                          value={stats.judged || 0}
                          valueStyle={{ color: isDarkMode ? '#ae81ff' : '#722ed1' }}
                      />
                    </Card>
                  </Col>
                </Row>

                <Card
                    bodyStyle={{ padding: 16 }}
                    className={isDarkMode ? "bg-[#3c3d32] border border-[#49483e] mb-6" : "bg-white mb-6"}
                >
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className={`block text-sm font-medium mb-1 ${isDarkMode ? "text-[#f8f8f2]" : "text-gray-700"}`}>
                        Filter by Keyword
                      </label>
                      <Input
                          value={filter.keyword}
                          onChange={e => handleFilterChange('keyword', e.target.value)}
                          placeholder="Search keyword..."
                          allowClear
                      />
                    </div>

                    <div>
                      <label className={`block text-sm font-medium mb-1 ${isDarkMode ? "text-[#f8f8f2]" : "text-gray-700"}`}>
                        Filter by Tools
                      </label>
                      <Input
                          value={filter.tools}
                          onChange={e => handleFilterChange('tools', e.target.value)}
                          placeholder="Search tools..."
                          allowClear
                      />
                    </div>

                    <div className="flex items-end space-x-2">
                      <Button
                          type="primary"
                          onClick={handleQuery}
                          className="w-1/2"
                      >
                        Apply
                      </Button>
                      <Button
                          onClick={handleClearFilters}
                          className="w-1/2"
                      >
                        Reset
                      </Button>
                    </div>
                  </div>
                </Card>

                <Card
                    bodyStyle={{ padding: 0 }}
                    className={isDarkMode ? "bg-[#3c3d32] border border-[#49483e]" : "bg-white"}
                >
                  <Table
                      columns={columns}
                      dataSource={allEvaluations.map(e => ({ ...e, key: e.id }))}
                      pagination={false}
                      scroll={{ x: 1500 }}
                      loading={isLoading}
                      onRow={(record) => ({
                        onClick: () => handleRowClick(record.id)
                      })}
                      rowClassName={`cursor-pointer ${isDarkMode ? "hover:bg-[#49483e]" : "hover:bg-blue-50"}`}
                  />

                  <div className={`mt-6 flex justify-between items-center p-4 ${isDarkMode ? "bg-[#3c3d32]" : "bg-gray-50"}`}>
                    <div className="flex items-center">
                      <span className={`mr-2 ${isDarkMode ? "text-[#f8f8f2]" : "text-gray-700"}`}>Items per page:</span>
                      <Select
                          value={pageSize}
                          style={{ width: 120 }}
                          onChange={(value) => {
                            setPageSize(value);
                            setCurrentPage(1); // 重置到第一页
                          }}
                          options={[
                            { value: 20, label: "20 / page" },
                            { value: 50, label: "50 / page" },
                            { value: 100, label: "100 / page" }
                          ]}
                      />
                    </div>

                    <Pagination
                        current={currentPage}
                        pageSize={pageSize}
                        total={totalItems}
                        onChange={handlePageChange}
                        showTotal={(total) => (
                            <span className={isDarkMode ? "text-[#f8f8f2]" : "text-gray-700"}>
                      Total {total} items
                    </span>
                        )}
                        showSizeChanger={false}
                        className={isDarkMode ? "ant-pagination-dark" : ""}
                    />
                  </div>
                </Card>
              </>
          )}
        </div>
      </ConfigProvider>
  );
}

const GlobalStyles = () => (
    <style jsx global>{`
      body.light-mode {
        background-color: #ffffff;
        color: #333333;
        transition: background-color 0.3s ease;
      }

      body.dark-mode {
        background-color: #272822;
        color: #f8f8f2;
        transition: background-color 0.3s ease;
      }

      .ant-pagination-dark .ant-pagination-item a {
        color: #f8f8f2 !important;
      }

      .ant-pagination-dark .ant-pagination-item-active a {
        color: #272822 !important;
      }
    `}</style>
);

export default function HomePage() {
  return (
      <>
        <GlobalStyles />
        <HomePageContentWrapper />
      </>
  );
}