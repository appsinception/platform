import { Select, message } from "antd";
import * as React from "react";
import { LoadingOverlay } from "../../atoms";
import { IFlowConfig, IStatus } from "../../types";
import { useConfigStore } from "../../../hooks/store";
import { fetchJSON, getServerUrl } from "../../api_utils";
import { useSelector } from "react-redux";
import { Link } from "gatsby";
import { Square2StackIcon } from "@heroicons/react/24/outline";

const AgentsWorkflowView = () => {
  const [error, setError] = React.useState<IStatus | null>({
    status: true,
    message: "All good",
  });

  const [loading, setLoading] = React.useState(false);
  const workflowConfig = useConfigStore((state) => state.workflowConfig);
  const setWorkflowConfig = useConfigStore((state) => state.setWorkflowConfig);

  const loggedIn = useSelector(state => state.user.loggedIn);
  const serverUrl = getServerUrl();
  const listWorkflowsUrl = `${serverUrl}/agency/list`;

  const [workflowConfigs, setWorkflowConfigs] = React.useState<IFlowConfig[]>(
    []
  );

  const [selectedConfig, setSelectedConfig] = React.useState<number>(0);

  const fetchWorkFlow = () => {
    setError(null);
    setLoading(true);
    // const fetch;
    const payLoad = {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    };

    const onSuccess = (data: any) => {
      if (data && data.status) {
        // message.success(data.message);

        setWorkflowConfigs(data.data);
        if (data.data.length > 0) {
          setWorkflowConfig(data.data[0]);
        }
      } else {
        message.error(data.message);
      }
      setLoading(false);
    };
    const onError = (err: any) => {
      setError(err);
      message.error(err.message);
      setLoading(false);
    };
    fetchJSON(listWorkflowsUrl, payLoad, onSuccess, onError);
  };

  React.useEffect(() => {
    if (loggedIn) {
      // console.log("fetching messages", messages);
      fetchWorkFlow();
    }
  }, []);

  return (
    <div className=" mb-4 relative">
      {/* <div className="font-semibold pb-2 border-b">
        <Square2StackIcon className="h-5 w-5 inline-block mr-1" />
        Agents Workflow{" "}
      </div> */}
      <div className="text-sm mt-2 mb-2 pb-1  ">
        {" "}
        Please select an agent team to begin.{" "}
      </div>

      <div className="relative mt-2 ">
        <LoadingOverlay loading={loading} />

        {workflowConfigs && workflowConfigs.length > 0 && (
          <Select
            className="w-full"
            value={workflowConfigs[selectedConfig].name}
            onChange={(value: any) => {
              setSelectedConfig(value);
              setWorkflowConfig(workflowConfigs[value]);
            }}
            options={
              workflowConfigs.map((config, index) => {
                return { label: config.name, value: index };
              }) as any
            }
          />
        )}
        <div className="mt-2 text-xs">
          {" "}
          View all teams{" "}
          <span className="text-accent">
            {" "}
            <Link to="/build">here</Link>
          </span>{" "}
        </div>
      </div>
      {!workflowConfigs ||
        (workflowConfigs && workflowConfigs.length === 0 && (
          <div className="p-1 border rounded text-xs px-2 text-secondary">
            {" "}
            No agent teams found.
          </div>
        ))}
    </div>
  );
};
export default AgentsWorkflowView;
